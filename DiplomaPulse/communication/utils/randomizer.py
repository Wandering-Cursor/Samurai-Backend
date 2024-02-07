import random

NUMBER_LIKE = [
	"one",
	"first",
	"many",
	"second",
	"third",
	"few",
]

NOUNS = [
	"katana",
	"sakura",
	"gun",
	"kimono",
	"ronin",
	"sushi",
	"dojo",
	"obi",
	"zen",
	"tatami",
	"bushido",
	"origami",
	"imperator",
	"edo",
]

ADJECTIVES = [
	"red",
	"blue",
	"green",
	"yellow",
	"black",
	"white",
]

RARE_NAMES = [
	"phantom-thief",
	"killer-queen",
	"red-hot-chili-pepper",
	"old-gods-of-asgard",
	"the-world",
	"to-heaved-with-your-xxx",
	"become-as-gods",
	"snake-eater",
	"song-of-the-ancients",
	"red-like-roses",
]


def get_random_pass_name():
	"""
	Generates random passphrase like name for chat

	Note - there's 1% chance to get rare name, that is not actually random
	"""
	rng = random.random()
	if rng < 0.01:
		return random.choice(RARE_NAMES)
	selection = [
		random.choice(NUMBER_LIKE),
		random.choice(ADJECTIVES),
		random.choice(NOUNS),
	]
	return "-".join(selection)
