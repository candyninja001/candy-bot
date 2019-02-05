import discord

TOKEN = ''
SERVER_DATA = {}

client = discord.Client()

def get_server_data(server):
    if server.id not in SERVER_DATA:
        load_server_data(server)
    return SERVER_DATA[server.id]
        

def load_server_data(server):
    server_id = server.id
    server_data = None
    file = None
    try:
        file = open('data/{server_id}.text')
        server_data = json.loads(file)
        file.close()
    except:
        if server_data == None:
            server_data = {}
        if file != None:
            file.close()
    SERVER_DATA[server_id] = server_data


def save_server_data():
    for server_id,server_data in SERVER_DATA.items():
        try:
            file = open('data/{server_id}.text', 'w')
            json.dump(server_data, file)
            file.close()
        except:
            if file != None:
                file.close()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!allow-role'):
        role_name = message.content[len('!allow-role'):].split()
        server_roles = message.server.roles
        role = None
        if len(role_name) != 0:
            for role in server_roles:
                if role_name == role.name.split():
                    role = role;
                    break
        if role == None:
            await client.send_message(message.channel, 'You must add the name of a role to allow')
            return
        get_server_data(message.server)
        if 'self-assigned-roles' not in SERVER_DATA[server.id]:
            SERVER_DATA[server.id]['self-assigned-roles'] = []
        SERVER_DATA[server.id]['self-assigned-roles'].append(role.id)
        msg = '{0.author.mention}'.format(message)

    if message.content.startswith('!role'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

try:
    token_file = None
    TOKEN = ''
    try:
        token_file = open('token.txt')
        TOKEN = token_file.read()
        token_file.close()
    except:
        if token_file != None:
            token_file.close()
            del token_file
    client.run(TOKEN)
except:
    print('Logging out')
    client.logout()
    print('Saving data')
    save_server_data()
