from garmin_fit_sdk import Decoder, Stream

stream = Stream.from_file("fitfiletools.fit")
decoder = Decoder(stream)
messages, errors = decoder.read()

max_depth = 0
for record in messages.get("record_mesgs", []):
    max_depth = max(max_depth, record["depth"])

# print(record["timestamp"], record["depth"])
print(max_depth)

# print(errors)
# print(messages)
