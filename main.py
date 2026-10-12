import json
import os

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class chatApp:
    def __init__(self):
        self.users = {}
        self.messages = []
        self.groups = {} 
        self.load_data()   

    def save_data(self):
        data = {
            "users": {
                username: user.password
                for username, user in self.users.items()
            },
            "messages": self.messages,
            "groups": self.groups
        }

        with open("chat_data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)


    def load_data(self):
        if not os.path.exists("chat_data.json"):
            return

        try:
            with open("chat_data.json", "r", encoding="utf-8") as file:
                data = json.load(file)

            self.users = {
                username: User(username, password)
                for username, password in data.get("users", {}).items()
            }

            self.messages = data.get("messages", [])
            self.groups = data.get("groups", {})

        except (json.JSONDecodeError, OSError):
            print("Warning: Could not load chat_data.json")

    def register(self):
        username = input("Enter username: ").strip()

        if not username:
            print("Username cannot be empty.")
            return

        if username in self.users:
            print("Username already exists.")
            return

        password = input("Enter password: ")

        if not password.strip():
            print("Password cannot be empty.")
            return

        self.users[username] = User(username, password)
        self.save_data()

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        if username in self.users and self.users[username].password == password:
            print("Login successful!")
            return username
        else:
            print("Invalid username or password.")
            return None

    def logged_in_menu(self, current_user):
        while True:
            print(f"-----Welcome {current_user}-----")
            print("1. Send Message ")
            print("2. View Messages ")
            print("3. Create Group ")
            print("4. Search Messages ")
            print("5. Logout ")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.send_message(current_user)
          
            elif choice == "2":
                print("Messages:")

                for msg in self.messages:
                    recipient = msg["recipientId"]

                    is_direct = (
                        msg["senderId"] == current_user
                        or recipient == current_user
                    )

                    is_group = (
                        recipient in self.groups
                        and current_user in self.groups[recipient]
                    )

                    if is_direct or is_group:
                        print(
                            f"From {msg['senderId']} "
                            f"to {recipient}: {msg['messageContent']}"
                        )

            elif choice == "3":
                group_name = input("Enter group name: ")
                members = input("Enter member usernames (comma-separated): ").split(",")
                members.append(current_user)  
                self.create_group(group_name, members)
            elif choice == "4":
                search_term = input("Enter search term: ")
                print("Search results:")
                self.search_messages(current_user, search_term)
            elif choice == "5":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    
    def send_message(self, sender_id):
        receiver_id = input("Enter receiver/group name: ").strip()

        if receiver_id in self.groups:
            if sender_id not in self.groups[receiver_id]:
                print("You are not a member of this group.")
                return
        elif receiver_id not in self.users:
            print("Receiver does not exist.")
            return

        message = input("Enter your message: ").strip()

        if not message:
            print("Message cannot be empty.")
            return

        self.messages.append({
            "senderId": sender_id,
            "recipientId": receiver_id,
            "messageContent": message
        })
        self.save_data()
        print("Message sent successfully!")



    
    def create_group(self, group_name, members):
        group_name = group_name.strip()

        if not group_name:
            print("Group name cannot be empty.")
            return

        if group_name in self.groups or group_name in self.users:
            print("Group name already exists.")
            return

        valid_members = []

        for member in members:
            member = member.strip()

            if member in self.users and member not in valid_members:
                valid_members.append(member)

        if len(valid_members) < 2:
            print("A group needs at least 2 registered members.")
            return

        self.groups[group_name] = valid_members
        self.save_data()

        print(f"Group '{group_name}' created successfully!")
        print("Members:", ", ".join(valid_members))


  
    def search_messages(self, user_id, search_term):
        filter_id = input(
            "Filter by sender/recipient/group (blank for all): "
        ).strip()

        for msg in self.messages:
            is_related = (
                msg["senderId"] == user_id
                or msg["recipientId"] == user_id
                or (
                    msg["recipientId"] in self.groups
                    and user_id in self.groups[msg["recipientId"]]
                )
            )

            if not is_related:
                continue

            if filter_id and filter_id not in [
                msg["senderId"], msg["recipientId"]
            ]:
                continue

            if search_term.lower() in msg["messageContent"].lower():
                print(
                    f"From {msg['senderId']} to "
                    f"{msg['recipientId']}: {msg['messageContent']}"
                )

    
    def start(self):
        while True:
            print("-----ChatApp-----")
            print("1. Register ")
            print("2. Login ")
            print("3. Exit ")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.register()
            elif choice == "2":
                current_user = self.login()
                if current_user:
                    self.logged_in_menu(current_user)
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")

app = chatApp()
app.start()