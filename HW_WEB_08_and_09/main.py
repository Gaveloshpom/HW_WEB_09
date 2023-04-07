import connect
from models import Author, Quotes


def find_by_tag(tags: list):
    tag = tags[0]
    data = Quotes.objects()
    for k in data:
        for t in k.tags:
            if t == tag:
                return k.quote


def find_by_tags(tags: list):
    result = []
    data = Quotes.objects()
    for k in data:
        if set(tags).intersection(k.tags):
            result.append(k.quote)
    return result


def find_by_name(name: list):
    result = []
    name_ = name[0]
    data = Quotes.objects()
    for k in data:
        if name_ == k.author.fullname:
            result.append(k.quote)
    return result


commands = {
    "tag": find_by_tag,
    "tags": find_by_tags,
    "name": find_by_name,
}


def main():
    while True:
        input_ = input("Вкажіть команду та аргументи: ")
        parsed = input_.split(":")
        if len(parsed) > 1:
            command = parsed[0].strip()
            arguments = [n.strip() for n in input_.split(":")[1:][0].split(",")]
        else:
            command = input_

        if command in commands.keys():
            print(commands[command](arguments))
        elif command == "exit":
            break
        else:
            print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
