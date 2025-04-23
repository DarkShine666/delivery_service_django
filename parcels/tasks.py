from decimal import Decimal, ROUND_HALF_UP
import logging
import requests
import redis
from django.conf import settings
from celery import shared_task
from parcels.models import Parcel


logger = logging.getLogger("parcels")

CBR_URL = "https://www.cbr-xml-daily.ru/daily_json.js"
CACHE_KEY = "usd_exchange_rate"
CACHE_TTL = 300  # 5 минут


def get_usd_exchange_rate():
    try:
        r = redis.Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True
        )

        cached_rate = r.get(CACHE_KEY)
        if cached_rate:
            logger.info("💰 Курс взят из кеша Redis")
            return Decimal(cached_rate)

        response = requests.get(CBR_URL, timeout=5)
        response.raise_for_status()
        value = response.json()["Valute"]["USD"]["Value"]
        usd_rate = Decimal(str(value))
        r.set(CACHE_KEY, str(usd_rate), ex=CACHE_TTL)
        logger.info(f"💰 Новый курс получен с ЦБ РФ: {usd_rate}")
        return usd_rate

    except Exception as e:
        logger.warning(f"❗ Ошибка получения курса доллара: {e}")
        return Decimal("90.0")  # запасной курс


@shared_task
def calculate_delivery_price(parcel_id: int):
    try:
        logger.debug(f"calculate_delivery_price: получаем посылку {parcel_id}")
        parcel = Parcel.objects.get(id=parcel_id)
        usd_rate = get_usd_exchange_rate()

        logger.debug(f"Текущий курс: {usd_rate}")
        logger.debug(
            f"Параметры: weight={parcel.weight_kg}, declared={parcel.declared_value_usd}"
        )
        weight = Decimal(str(parcel.weight_kg))
        declared = Decimal(str(parcel.declared_value_usd))
        base_usd = weight * Decimal("0.5") + declared * Decimal("0.01")

        price_rub = (base_usd * usd_rate).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        parcel.delivery_price = price_rub
        parcel.save()

        logger.info(f"📦 Обновлена посылка {parcel_id} — {price_rub} RUB")
        logger.info(f"📦 Посылка {parcel_id} — расчет окончен: {price_rub} RUB")
        return f"Updated parcel {parcel_id} with price {price_rub} RUB"

    except Parcel.DoesNotExist:
        logger.error(f"❌ Parcel {parcel_id} does not exist")
        return f"Parcel {parcel_id} does not exist"
    except Exception as e:
        logger.error(f"❌ Error updating parcel {parcel_id}: {e}")
        return f"Error updating parcel {parcel_id}"


@shared_task
def recalculate_pending_parcels():
    logger.info("Старт recalculate_pending_parcels")
    pending = Parcel.objects.filter(delivery_price__isnull=True)
    logger.info(f"Нужно пересчитать {pending.count()} посылок")
    for p in pending:
        calculate_delivery_price.delay(p.id)
    logger.info("Задачи на пересчет отправлены")
