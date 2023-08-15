# Import libraries
import discord
from discord.ext import commands
from discord.ext.commands import Context
import mysql.connector
import asyncio

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
bot = commands.Bot(intents=intents)

# MySQL database configuration
db_config = {
    'host': '78.108.218.47',
    'user': 'u102510_h0ykZunzcZ',
    'password': 'i+k7kMNnHp!UI0ZHlInfmFWG',
    'database': 's102510_Files'
}

# Validation and feedback logic for each question


def validate_response_with_feedback(idx, response):
    feedback = None
    validated_response = response.strip()

    if idx == 0:
        if not validated_response.lower().startswith("tbd"):
            feedback = f"Invalid response. Please start with 'TBD' if unknown."
    elif idx == 1:
        if validated_response.lower() not in ["male", "female", "other"]:
            feedback = f"Invalid response. Please enter 'Male', 'Female', or 'Other'."
    elif idx == 2:
        if not validated_response:
            feedback = f"Invalid response. Please enter the full name."
    elif idx == 3:
        if not validated_response.isdigit() or int(validated_response) <= 0:
            feedback = f"Invalid response. Please enter a valid age in years."
    elif idx == 4:
        if not validated_response:
            feedback = f"Invalid response. Please enter the nationality."
    elif idx == 5:
        if not validated_response.startswith("#") or (not validated_response.endswith("cm") and not validated_response.endswith('"')):
            feedback = f"Invalid response. Please enter the height in the format of '#cm' or '#'#'\"'."
    elif idx == 6:
        if not validated_response:
            feedback = f"Invalid response. Please enter the occupation."
    elif idx == 7:
        if validated_response.lower() not in ["yes", "no", "tbd"]:
            feedback = f"Invalid response. Please enter 'Yes', 'No', or 'TBD'."
    elif idx == 8:
        if not validated_response.isdigit():
            feedback = f"Invalid response. Please enter a valid phone number. Ex: 1234567890"
    elif idx == 9:
        if not validated_response:
            feedback = f"Invalid response. Please enter any details."
    elif idx == 10:
        if validated_response.lower() not in ["yes", "no", "tbd"]:
            feedback = f"Invalid response. Please enter 'Yes', 'No', or 'TBD'."
    elif idx == 11:
        if not validated_response:
            feedback = f"Invalid response. Please enter the known addresses."
    elif idx == 12:
        if not validated_response:
            feedback = f"Invalid response. Please enter any encounters."
    # ... (other questions)

    return validated_response, feedback


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.slash_command(name="createfile", guild_ids=[1105196644808527872])
async def createfile(ctx: Context):
    await ctx.send("Starting file creation.")

    questions = [
        "Please enter the character's IGN. If unknown, type TBD.",
        "Please enter the character's sex as **Male**, **Female**, or **Other**. If unknown, type TBD.",
        "Please enter the character's full name. If unknown, type TBD.",
        "Please enter the character's age in years. If unknown, type TBD.",
        "Please enter the character's nationality. If unknown, type TBD.",
        "Please enter the character's height as #cm or #'#\". If unknown, type TBD.",
        "Please enter the character's occupation. If unknown, type TBD.",
        "Is the character affiliated with any gangs? Yes, No, or TBD. If unknown, type TBD.",
        "Please enter the character's phone number. If unknown, type TBD.",
        "Please enter any details about the character. If none, type TBD.",
        "Is the character associated with anyone? If none or unknown, type TBD.",
        "What are the known addresses for this person? If unknown, type TBD.",
        "Please list any encounters you have had with this character. If none, type TBD."
    ]

    answers = []

    for idx, question in enumerate(questions):
        question_message = await ctx.send(question)

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        try:
            response = await bot.wait_for('message', timeout=60.0, check=check)
            await response.delete()

            if response.content.lower() == 'cancel':
                await question_message.delete()
                await ctx.send("File creation canceled.")
                return
            else:
                validated_response, feedback = validate_response_with_feedback(idx, response.content)
                if validated_response is None:
                    await ctx.send(feedback)
                    return
                answers.append(validated_response)

            await question_message.delete()
        except asyncio.TimeoutError:
            await question_message.delete()
            await ctx.send("Ran out of time. Profile creation canceled.")
            return

    try:
        db_connection = mysql.connector.connect(**db_config)
        db_cursor = db_connection.cursor()

        # Create the table if it doesn't exist
        create_table_query = """CREATE TABLE IF NOT EXISTS files (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ign VARCHAR(16),
            sex VARCHAR(6),
            full_name VARCHAR(100),
            age INT(3),
            nationality VARCHAR(50),
            height VARCHAR(5),
            occupation VARCHAR(50),
            gang_affiliation SET('TBD', 'Yes', 'No'),
            phone_number VARCHAR(12),
            details TEXT,
            associates TEXT,
            addresses TEXT,
            encounters MEDIUMTEXT,
            clearance_level VARCHAR(255)
        )"""
        db_cursor.execute(create_table_query)

        query = ("INSERT INTO files (ign, sex, full_name, age, nationality, height, occupation, gang_affiliation, "
                 "phone_number, details, associates, addresses, encounters) VALUES (%s, %s, %s, %s, "
                 "%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        values = answers

        db_cursor.execute(query, values)
        db_connection.commit()

        db_cursor.close()
        db_connection.close()

        await ctx.send("Profile created successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")  # Debug statement
        await ctx.send("An error occurred while creating the profile. Please try again.")
        return

bot.run('MTEzNDE4Nzc0ODAyMzA4MzE2MA.GUe0Sk.9uEQfzYsj1AhKFNX8zwx864Toj999_cBO10Kc0')
