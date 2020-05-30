from DevGossip import DevGossip

print("Welcome to DevGossip")

app = DevGossip()
app.homepage()

while True:
    app.get_user_input()
