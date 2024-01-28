import discord
from discord.ext import commands
import math

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


def caesar_cipher(text, key, decrypt=False):
    result = ''
    for char in text:
        if char.isalpha():
            shift = ord('a') if char.islower() else ord('A')
            if decrypt:
                result += chr((ord(char) - shift - key) % 26 + shift)
            else:
                result += chr((ord(char) - shift + key) % 26 + shift)
        else:
            result += char
    return result


def affine_cipher(text, key_a, key_b, decrypt=False):
    if mod_inverse(key_a, 26) is None:
        raise commands.BadArgument("Invalid key_a value. Ensure it is coprime with 26.")

    result = ''
    for char in text:
        if char.isalpha():
            shift = ord('a') if char.islower() else ord('A')
            if decrypt:
                result += chr((mod_inverse(key_a, 26) * (ord(char) - shift - key_b)) % 26 + shift)
            else:
                result += chr((key_a * (ord(char) - shift) + key_b) % 26 + shift)
        else:
            result += char
    return result


def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None


@bot.command(name='gcd')
async def calculate_gcd(ctx, a: int, b: int):
    try:
        result = math.gcd(a, b)  # Use math.gcd to calculate GCD
        await ctx.send(f'The GCD of {a} and {b} is: {result}')
    except commands.BadArgument as e:
        await ctx.send(f'Error: {e}')


@bot.command(name='mod_inverse')
async def calculate_mod_inverse(ctx, a: int, m: int):
    try:
        result = mod_inverse(a, m)
        if result is not None:
            await ctx.send(f'The multiplicative inverse of {a} modulo {m} is: {result}')
        else:
            await ctx.send(f'The multiplicative inverse does not exist for {a} modulo {m}.')
    except commands.BadArgument as e:
        await ctx.send(f'Error: {e}')


@bot.command(name='encrypt_caesar')
async def encrypt_caesar(ctx, key: int, *, text: str):
    try:
        encrypted_text = caesar_cipher(text, key)
        await ctx.send(f'Caesar Encrypted text: {encrypted_text}')
    except commands.BadArgument as e:
        await ctx.send(f'Error: {e}')


@bot.command(name='decrypt_caesar')
async def decrypt_caesar(ctx, key: int, *, text: str):
    try:
        decrypted_text = caesar_cipher(text, key, decrypt=True)
        await ctx.send(f'Caesar Decrypted text: {decrypted_text}')
    except commands.BadArgument as e:
        await ctx.send(f'Error: {e}')


@bot.command(name='encrypt_affine')
async def encrypt_affine(ctx, key_a: int, key_b: int, *, text: str):
    try:
        encrypted_text = affine_cipher(text, key_a, key_b)
        await ctx.send(f'Affine Encrypted text: {encrypted_text}')
    except commands.BadArgument as e:
        await ctx.send(f'Error: {e}')


@bot.command(name='decrypt_affine')
async def decrypt_affine(ctx, key_a: int, key_b: int, *, text: str):
    try:
        decrypted_text = affine_cipher(text, key_a, key_b, decrypt=True)
        await ctx.send(f'Affine Decrypted text: {decrypted_text}')
    except commands.BadArgument as e:
        await ctx.send(f'Error: {e}')


@bot.command(name='bruteforce')
async def bruteforce_caesar(ctx, *, text: str):
    try:
        with open("en-basic.txt", "r", encoding="utf-8") as file:
            possible_words = [word.strip().lower() for word in file.readlines()]

        found_words_list = []

        for key in range(26):
            decrypted_text = caesar_cipher(text, key, decrypt=True)
            await ctx.send(f'Attempting Caesar Decryption with Key {key}: {decrypted_text}')

            found_words = [word for word in possible_words if len(word) == len(text) and word in decrypted_text.lower()]

            if found_words:
                found_words_list.extend(found_words)

        if found_words_list:
            await ctx.send(f'\nSuccess! Common Words Found: {", ".join(found_words_list)}')
        else:
            await ctx.send('Unsuccessful. No valid decryption found.')

    except commands.BadArgument as e:
        await ctx.send(f'Error: {e}')
    except FileNotFoundError:
        await ctx.send('Error: Word file not found.')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

token = 'MTIwMDExNDQ3MjIzMzIwNTg0MQ.G1alMe.3Sszy_GrV20PFtO9zfMvjTomyR1JQCFyjIUiew'
bot.run(token)
