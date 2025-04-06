import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.lines as mlines
import schedulebuilder as sc  # Make sure this imports the right function!

def draw_class_to_career_map(class_to_goals):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')

    # Data prep
    classes = list(class_to_goals.keys())
    all_goals = sorted(set(goal for goals in class_to_goals.values() for goal in goals))

    class_y = {cls: i for i, cls in enumerate(reversed(classes))}
    goal_y = {goal: i for i, goal in enumerate(reversed(all_goals))}

    # Positioning
    x_class = 0.1
    x_goal = 0.8
    box_width = 0.15
    box_height = 0.6

    # Store box positions for arrow endpoints
    class_boxes = {}
    goal_boxes = {}

    # Draw class rectangles
    for cls, y in class_y.items():
        y_pos = y * 1.5
        box = FancyBboxPatch((x_class, y_pos), box_width, box_height,
                             boxstyle="round,pad=0.02", fc="lightblue", ec="black")
        ax.add_patch(box)
        ax.text(x_class + box_width / 2, y_pos + box_height / 2, cls, ha='center', va='center', fontsize=10)
        class_boxes[cls] = (x_class + box_width, y_pos + box_height / 2)

    # Draw goal rectangles
    for goal, y in goal_y.items():
        y_pos = y * 1.5
        box = FancyBboxPatch((x_goal, y_pos), box_width, box_height,
                             boxstyle="round,pad=0.02", fc="lightgreen", ec="black")
        ax.add_patch(box)
        ax.text(x_goal + box_width / 2, y_pos + box_height / 2, goal, ha='center', va='center', fontsize=10)
        goal_boxes[goal] = (x_goal, y_pos + box_height / 2)

    # Draw arrows
    for cls, goals in class_to_goals.items():
        start_x, start_y = class_boxes[cls]
        for goal in goals:
            end_x, end_y = goal_boxes[goal]
            ax.annotate('', 
                        xy=(end_x, end_y), 
                        xytext=(start_x, start_y), 
                        arrowprops=dict(arrowstyle='->', color='gray'))

    ax.set_xlim(0, 1.1)
    ax.set_ylim(-1, max(len(classes), len(all_goals)) * 2)

    plt.tight_layout()
    plt.show()


def make_connections(interests, term):
    # Fetch scheduled classes and metadata
    class_schedule, course_metadata = sc.schedule_build(interests, term)
    lst=list(class_schedule.keys())
    dic={}
    for i in lst:
        dic[i]=('Required for Major')
    # print(lst)
    # Convert metadata to class_to_goals format
    course_metadata.update(dic)
    class_to_goals = {}
    for course, goals in course_metadata.items():
        # Extract course code (e.g., 'FRIT-M 110' from full name)
        code = course.split()[0]  # Simple split; adjust as needed
        class_to_goals[code] = goals
    
    draw_class_to_career_map(class_to_goals)



# Example usage:
make_connections([''], 1)  # Adjust your interests and term
