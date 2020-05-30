from DevGossip import DevGossip

def main():
	print("Welcome to DevGossip")

	app = DevGossip()
	app.homepage()

	while True:
	    app.get_user_input()


if __name__ == '__main__':
	main()
