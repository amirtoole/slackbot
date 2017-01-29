import logging
import re
import sys

from slackbot import settings
from slackbot.bot import Bot, respond_to
from slackbot.slackclient import SlackClient

from slackbot_settings import API_TOKEN
from utils.weather import City, CityIndex

WEATHER = 'weather'
CITYINDEX = CityIndex()


def main():
    kw = {
        'format': '[%(asctime)s] | %(name)s | %(levelname)s | %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': logging.DEBUG if settings.DEBUG else logging.INFO,
        'stream': sys.stdout,
    }
    logging.basicConfig(**kw)
    logging.getLogger('requests.packages.urllib3.connectionpool') \
        .setLevel(logging.WARNING)
    bot = Bot()
    bot.run()


@respond_to('hi', re.IGNORECASE)
def hi(message):
    message.reply('Hi!')
    # react with thumb up emoji
    message.react('+1')


@respond_to(WEATHER, re.IGNORECASE)
def weather(message):
    # remove 'weather ' from message
    cityStr = message.body['text'][len(WEATHER):].strip()

    if not CITYINDEX.is_city(cityStr):
        message.reply("Couldn't find your city: " + cityStr)
        return

    city = City(CITYINDEX.data_url(cityStr))
    message.reply('Weather in %s, %s\nCurrent: %s °C\nForecast: %s' % (cityStr,
                                                                   CITYINDEX.province(cityStr),
                                                                   city.get_quantity('currentConditions/temperature'),
                                                                   city.get_quantity('forecastGroup/forecast/textSummary')))

    #TODO: convert keywords of forecastGroup/forecast/textSummary into appropriate emoji?

# broadcast online status to general channel
def greetGeneralChannel():
    client = SlackClient(API_TOKEN)
    client.send_message(client.find_channel_by_name('general'), 'hey general!')
    client.rtm_read()


if __name__ == "__main__":
    # greetGeneralChannel()
    main()
