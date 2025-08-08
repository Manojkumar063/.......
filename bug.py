import json
import datetime
import os

class Bug:
    def __init__(self, bug_id, description, priority='medium', status='open'):
        self.bug_id = bug_id
        self.description = description
        self.priority = priority  # low, medium, high
        self.status = status  # open, in progress, closed
        self.created_at = datetime.datetime.now()
        self.updated_at = self.created_at

    def update_status(self, new_status):
        self.status = new_status
        self.updated_at = datetime.datetime.now()

    def to_dict(self):
        return {
            'bug_id': self.bug_id,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        bug = cls(data['bug_id'], data['description'], data['priority'], data['status'])
        bug.created_at = datetime.datetime.fromisoformat(data['created_at'])
        bug.updated_at = datetime.datetime.fromisoformat(data['updated_at'])
        return bug

class BugTracker:
    def __init__(self, filename='bugs.json'):
        self.filename = filename
        self.bugs = []
        self.next_id = 1
        self.load()

    def add_bug(self, description, priority='medium'):
        bug = Bug(self.next_id, description, priority)
        self.bugs.append(bug)
        self.next_id += 1
        self.save()
        print(f"Bug added: ID {bug.bug_id}")

    def list_bugs(self):
        if not self.bugs:
            print("No bugs tracked yet.")
            return
        for bug in self.bugs:
            print(f"ID: {bug.bug_id} | Description: {bug.description} | Priority: {bug.priority} | Status: {bug.status}")
            print(f"Created: {bug.created_at} | Updated: {bug.updated_at}")
            print("-" * 40)

    def update_bug(self, bug_id, new_status):
        for bug in self.bugs:
            if bug.bug_id == bug_id:
                bug.update_status(new_status)
                self.save()
                print(f"Bug {bug_id} updated to {new_status}")
                return
        print(f"Bug {bug_id} not found.")

    def delete_bug(self, bug_id):
        self.bugs = [bug for bug in self.bugs if bug.bug_id != bug_id]
        self.save()
        print(f"Bug {bug_id} deleted.")

    def save(self):
        data = [bug.to_dict() for bug in self.bugs]
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.bugs = [Bug.from_dict(d) for d in data]
                if self.bugs:
                    self.next_id = max(bug.bug_id for bug in self.bugs) + 1

def main():
    tracker = BugTracker()
    while True:
        print("\nBug Tracker Menu:")
        print("1. Add Bug")
        print("2. List Bugs")
        print("3. Update Bug Status")
        print("4. Delete Bug")
        print("5. Exit")
        choice = input("Enter choice: ")
        
        if choice == '1':
            desc = input("Enter bug description: ")
            prio = input("Enter priority (low/medium/high, default medium): ") or 'medium'
            tracker.add_bug(desc, prio)
        elif choice == '2':
            tracker.list_bugs()
        elif choice == '3':
            bug_id = int(input("Enter bug ID: "))
            status = input("Enter new status (open/in progress/closed): ")
            tracker.update_bug(bug_id, status)
        elif choice == '4':
            bug_id = int(input("Enter bug ID to delete: "))
            tracker.delete_bug(bug_id)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
