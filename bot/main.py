# Import libraries
import discord
from discord.ext import commands
from discord.ext.commands import Context
import mysql.connector
import asyncio
import re


# Define variables
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
bot = commands.Bot(intents=intents)
error_channel_id = 1135721885208940625


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

    print(f"Validating response for question {idx}: {validated_response}")  # Add this line

    if idx == 0:
        if len(validated_response) > 16:
                feedback = f"Invalid response. Please enter up to 16 characters."
        elif not re.match(r'^[a-zA-Z0-9-_]+$', validated_response):
                feedback = f"Invalid response. Please use only alphanumeric characters, hyphens, and underscores."
                validated_response = None
    elif idx == 1:
        if validated_response.lower() not in ["male", "female", "other", "tbd"]:
                feedback = f"Invalid response. Please enter 'Male', 'Female', or 'Other'. Enter 'TBD' if unknown."
                validated_response = None
    elif idx == 2:
        if not re.match(r'^[a-zA-ZÀ-ÖØ-öø-ÿ ]+$', validated_response):
                feedback = f"Invalid response. Please use only letters and accented characters."
                validated_response = None
    elif idx == 3:
        if not validated_response.isdigit() or int(validated_response) <= 0:
                feedback = f"Invalid response. Please enter a valid age in years."
                validated_response = None
    elif idx == 4:
        if not re.match(r'^[a-zA-ZÀ-ÖØ-öø-ÿ ]+$', validated_response):
                feedback = f"Invalid response. Please use only letters and accented characters. Ex: half German half Japanese. Do not include any punctuation."
                validated_response = None
    elif idx == 5:
        if not (validated_response.endswith("cm") or validated_response.endswith('"')):
                feedback = f"Invalid response. Please enter the height in the format of '#cm' or '#'#\"'."
                validated_response = None
    elif idx == 6:
        if not re.match(r'^[A-Za-zÀ-ÿ\s\-\.,;:!?"\'()]+$', validated_response):
                feedback = f"Invalid response. Please use only letters, accented characters, punctuation, spaces, hyphens, and common punctuation marks."
    elif idx == 7:
        if validated_response.lower() not in ["yes", "no", "tbd"]:
                feedback = f"Invalid response. Please enter 'Yes', 'No', or 'TBD'."
                validated_response = None
    elif idx == 8:
        if not re.match(r'^[0-9\-]+$', validated_response):
                feedback = f"Invalid response. Please use only numbers and hyphens. Example: 123-456-7890"
                validated_response = None

    print(f"Feedback for question {idx}: {feedback}")

    return validated_response, feedback


@bot.event
async def on_ready():
    try:
        print(f'Logged in as {bot.user.name}')

        channel_id = 1135721885208940625
        channel = bot.get_channel(channel_id)

        if channel:
            await channel.send(
                content=f"Successfully logged in as {bot.user.name}. Developer mode: `ENABLED`. Version control: `Alpha 0.0.1`")
        else:
            print("Channel not found.")
    except Exception as e:
        print(f"An error occurred in on_ready: {e}")


@bot.event
async def on_error(ctx, event, error, *args, **kwargs):
    if isinstance(error, commands.CommandError):
        try:
            error_msg = f"An error occurred in event {event}: {args[0]}"
            print(error_msg)
            error_channel = bot.get_channel(error_channel_id)
            if error_channel:
                await error_channel.send(error_msg)
            else:
                print("Error channel not found")
        except Exception as e:
            print(f"An error occurred in on_command_error: {e}")


try:
    @bot.slash_command(name="createfile", description="Create a new character file or update an existing one.", guild_ids=[1105196644808527872])
    async def createfile(ctx: Context):
        create_confirmation = await ctx.respond("Starting file creation.")
        invalid_message = None

        questions = [
            "Please enter the character's IGN. If unknown, type TBD.",
            "Please enter the character's sex as **Male**, **Female**, or **Other**. If unknown, type **TBD.**",
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
            "Please describe any encounters you have had with this character. If none, type TBD."
        ]

        answers = []

        idx = 0  # Initialize question index

        while idx < len(questions):
            question = questions[idx]
            question_message = await ctx.send(question)

            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel

            if invalid_message:
                await invalid_message.delete()
                invalid_message = None  # Reset the invalid_message variable

            try:
                response = await bot.wait_for('message', timeout=60.0, check=check)
                await response.delete()

                if response.content.lower() == 'cancel':
                    await question_message.delete()
                    await create_confirmation.delete()
                    cancel_confirmation = await ctx.send("File creation canceled.")
                    countdown_msg = await ctx.send("This message will self-destruct in 10 seconds...")
                    for seconds_left in range(9, 0, -1):
                        await asyncio.sleep(1)
                        await countdown_msg.edit(content=f"This message will self-destruct in {seconds_left} seconds...")
                    await countdown_msg.delete()
                    await cancel_confirmation.delete()
                    return
                else:
                    if invalid_message:
                        await invalid_message.delete()  # Delete the previous invalid response message
                    validated_response, feedback = validate_response_with_feedback(idx, response.content)
                    if validated_response is None:
                        invalid_message = await ctx.send(feedback)
                    else:
                        answers.append(validated_response)
                        idx += 1  # Move to the next question
                        if invalid_message:
                            await invalid_message.delete()
                            invalid_message = None

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
                encounters MEDIUMTEXT
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
            event = "createfile"
            await ctx.send(f"An error occurred in event {event} while creating the profile: {e}")
            return

except Exception as e:
    async def send_error(event, args):
        error_channel = bot.get_channel(error_channel_id)
        if error_channel:
            error_message = f"Bot encountered an error in event '{event}': {args[0]}\nError: {e}"
            await error_channel.send(error_message)

    event = "unknown"  # Provide an event name if not available
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_error(event, (str(e),)))


async def delete_invalid_messages(messages):
    for message in messages:
        try:
            await message.delete()
        except discord.errors.NotFound:
            pass  # Message may have been deleted already


bot.run('TOKEN')
