import reminders
import datetime

def main():
	all_todo = reminders.get_reminders(completed=False)

	now = datetime.datetime.now()
	# Display open reminders with a due date per calendar
	all_calendars = reminders.get_all_calendars()
	for cal in all_calendars:
		print(f"\n{cal.title}\n" + '=' * 40)
		todo = reminders.get_reminders(calendar=cal, completed=False)
		for r in todo:
			due_date: datetime = r.due_date
			if due_date:
				text = f"[ ] {r.title} ({due_date.strftime('%a, %d.%m')})"
				print(text)


if __name__ == '__main__':
	main()
