import lambdawarmer
from mangum import Mangum

from app.main import create_app

# Serverless deploy
api = Mangum(create_app(add_middlewares=True), lifespan="off")


@lambdawarmer.warmer(delay=250)
def handler(event, context):
    return api(event, context)
