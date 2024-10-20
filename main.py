from memopin.tools import (
    tool_create_vector, tool_read_vector, tool_update_vector,
    tool_delete_vector, tool_chat, tool_upload_audio
)

def main():
    tools = {
        "create": tool_create_vector,
        "read": tool_read_vector,
        "update": tool_update_vector,
        "delete": tool_delete_vector,
        "chat": tool_chat,
        "upload": tool_upload_audio,
    }

    while True:
        action = input("Choose an action: 'create', 'read', 'update', 'delete', 'chat', 'upload', or 'exit': ").strip().lower()

        if action == 'exit':
            print("Exiting the program.")
            break
        elif action in tools:
            tools[action]()
        else:
            print("Invalid action. Please try again.")

if __name__ == "__main__":
    main()
