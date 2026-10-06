
from dataclasses import dataclass, field


@dataclass
class Task:
    name: str
    duration: int
    dependencies: list[str] = field(default_factory=list)


def calculate_schedule(tasks):
    task_map = {task.name: task for task in tasks}
    schedule = {}

    def calculate_finish(task_name, visiting=None):
        if visiting is None:
            visiting = set()

        if task_name in visiting:
            raise ValueError("Circular dependency detected.")

        if task_name in schedule:
            return schedule[task_name]

        if task_name not in task_map:
            raise ValueError(f"Unknown dependency: {task_name}")

        visiting = visiting | {task_name}
        task = task_map[task_name]

        start = 0
        for dependency in task.dependencies:
            finish = calculate_finish(dependency, visiting)
            start = max(start, finish)

        finish = start + task.duration
        schedule[task_name] = (start, finish)
        return finish

    for task in tasks:
        calculate_finish(task.name)

    return schedule


def main():
    tasks = [
        Task("Requirements", 2),
        Task("Design", 3, ["Requirements"]),
        Task("Development", 5, ["Design"]),
        Task("Testing", 2, ["Development"]),
        Task("Documentation", 3, ["Design"]),
    ]

    schedule = calculate_schedule(tasks)

    print("PROJECT SCHEDULE")
    print("-" * 55)
    print(f"{'Task':<20}{'Start':>10}{'Finish':>12}")

    for task in tasks:
        start, finish = schedule[task.name]
        print(f"{task.name:<20}{start:>10}{finish:>12}")

    total_duration = max(finish for _, finish in schedule.values())
    print("-" * 55)
    print(f"Estimated project duration: {total_duration} time units")


if __name__ == "__main__":
    main()
