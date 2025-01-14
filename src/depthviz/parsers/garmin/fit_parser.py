from garmin_fit_sdk import Decoder, Stream
from pprint import pprint
import math

stream = Stream.from_file("../../../../tests/data/garmin/14087156326_ACTIVITY.fit")
decoder = Decoder(stream)
messages, errors = decoder.read(convert_datetimes_to_dates=False)
file_type = messages.get("file_id_mesgs")[0].get("type")  # activity

sport = messages.get("sport_mesgs")[0].get(
    "sport"
)  # diving ; there is also one in lap_mesgs
# buttom time here is accurate
dive_summary = []
dive_summary_mesgs = messages.get("dive_summary_mesgs", [])

for dive_summary_mesg in dive_summary_mesgs:
    if dive_summary_mesg.get("reference_mesg") != "lap":
        continue
    lap_idx = dive_summary_mesg.get("reference_index")
    lap_mesg = messages.get("lap_mesgs")[lap_idx]
    bottom_time = dive_summary_mesg.get("bottom_time")
    start_time = lap_mesg.get("start_time")
    end_time = math.floor(start_time + bottom_time)
    dive_summary.append(
        {
            "start_time": start_time,
            "end_time": end_time,
            "max_depth": dive_summary_mesg.get("max_depth"),
            "avg_depth": dive_summary_mesg.get("avg_depth"),
            "bottom_time": bottom_time,
        }
    )
selected_dive_index = 8
records = messages.get("record_mesgs", [])

pprint(dive_summary[selected_dive_index])
# pprint(records)

MARGIN_START_TIME = 2
first_timestamp = None
previous_depth = None
is_dive_end = False
for record in records:
    if (
        record.get("timestamp")
        < dive_summary[selected_dive_index].get("start_time") - MARGIN_START_TIME
    ):
        continue
    # After the dive ends, get the depth until it starts to increase or is 0
    if (
        record.get("timestamp")
        >= dive_summary[selected_dive_index].get("end_time") - MARGIN_START_TIME
    ):
        is_dive_end = True
    if is_dive_end and record.get("depth") > previous_depth:
        break

    if first_timestamp is None:
        first_timestamp = record.get("timestamp")

    time = record.get("timestamp") - first_timestamp
    depth = record.get("depth")
    print(time, depth)
    previous_depth = record.get("depth")

    # When the dive reaches the buttom time, after that when the depth is 0, the dive is considered to be ended
    if is_dive_end and round(record.get("depth"), 3) == 0:
        break


# print(messages.keys())


# max_depth = 0
# for record in messages.get("record_mesgs", []):
#     max_depth = max(max_depth, record["depth"])

# print(record["timestamp"], record["depth"])
# print(max_depth)

# print(errors)
# print(messages)
