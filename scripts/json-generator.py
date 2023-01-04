import json


def main():
	json_data = {
		"fullkeepnet_orange": {
			"low": (250, 185, 0),
			"high": (260, 195, 5)
		},
		"hookedfish_blue": {
			"low": (27, 67, 193),
			"high": (37, 77, 203)
		}
	}

	with open("values.json", "w") as file:
		file.write(json.dumps(json_data, indent=4))


if __name__ == '__main__':
	main()
