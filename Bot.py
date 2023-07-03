import asyncio
import logging
import discord
import sys
import argparse
from discord.ext import commands
from utils import secrets


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--secrets-dir', type=str, required=True)
    return parser.parse_args()


async def start_bot(bot):
    args = parse_args()
    secret = secrets.SecretsReader(args.secrets_dir)
    #root = logging.getLogger()
    # handler = logging.StreamHandler(sys.stdout)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # handler.setFormatter(formatter)
    # root.addHandler(handler)
    logging.basicConfig(stream=sys.stdout)
    await bot.load_extension(f'cogs.audio')
    # await bot.tree.sync(guild = discord.Object())
    await bot.start(secret.get('token'))


if __name__ == '__main__':
    intens = discord.Intents.all()
    bot = commands.Bot(command_prefix='-', intents=intens)
    asyncio.run(start_bot(bot))