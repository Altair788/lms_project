import requests
import stripe
from rest_framework import status

from config.settings import CUR_API_KEY, CUR_API_URL, STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product_name):
    # Your code here
    product = stripe.Product.create(name=product_name)
    return product


def convert_rub_to_usd(rub_price):
    usd_price = 0
    response = requests.get(
        f"{CUR_API_URL}v3/latest?apikey={CUR_API_KEY}&currencies=RUB"
    )
    if response.status_code == status.HTTP_200_OK:
        usd_rate = response.json()["data"]["RUB"]["value"]
        usd_price = rub_price / usd_rate
    return int(usd_price)


def create_stripe_price(amount, product_id):
    """
    Создает новую цену в Stripe с указанной суммой.
    """

    price = stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product=product_id,
    )

    return price


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )

    return session.get("id"), session.get("url")


def get_session_data(session_id: str):
    try:
        session_data = stripe.checkout.Session.retrieve(session_id)
        return session_data
    except stripe.error.StripeError as e:
        print(f"Stripe error: {str(e)}")
        return None
