import json
import minizinc
from minizinc import Instance, Model, Solver
import numpy as np
from datetime import timedelta

# def runModel():
#     # Create a MiniZinc model
#     model = Model("./JEEC.mzn")
#     solver = Solver.lookup("gecode") # GECODE WORKS BEST WITH THIS IMPLEMENTATION
#     instance = Instance(solver, model)
#     instance.add_file("./JEECdata.dzn")

#     # Solve the model
#     result = instance.solve()
    
#     return result



def Read_file_json():
    # Define os dias da semana e horários possíveis
    weekdays = ["Saturday_1", "Sunday_1", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday_2", "Sunday_2"]
    shifts_list = ["8:00", "9:30", "11:00", "12:30", "14:00", "15:30", "17:00", "18:30", "20:00"]
    roles = ["Coordenator", "Webdev", "Marketing", "Business", "Logistics", "Speakers", "Volunteers"]
    people = []  # Lista para armazenar todas as instâncias de Person
    nShifts = len(weekdays) * len(shifts_list)
    shiftsWeek = []
    tags = []
    person_id = 0
    with open("testshifts.json", "r") as file:
        data = json.load(file)
        for person_data in data:
            name = person_data["member"]
            role_name = person_data["tag"]
            shifts = person_data["shifts"]
            person_shifts = []
            for weekday in shifts:
                if weekday in weekdays:
                    current_day_index = weekdays.index(weekday)
                    for shift in shifts[weekday]:
                        if shift in shifts_list:
                            shift_index = shifts_list.index(shift)
                            global_index = current_day_index * len(shifts_list) + shift_index + 1
                            person_shifts.append(global_index)

            tag = (roles.index(role_name) if role_name in roles else -1) + 1
            tags.append(tag)
            # print(name, ": " ,person_shifts)
            shiftsWeek.append(set(person_shifts))
            #person = Person(name, tag , person_shifts, person_id)
            #people.append(person)
            person_id += 1
    
    file.close()
    shiftsWeek = np.array(shiftsWeek)

    return shiftsWeek, tags, nShifts

def write_output_file(output_file, nPeople, nShifts, maxPerShift, nRoles, rolePeople, availability):


    with open(output_file, 'w') as file:
        file.write(f'num_people = {nPeople};\n')
        file.write(f'num_shifts = {nShifts};\n')
        file.write(f'max_people_per_shift = {maxPerShift};\n')
        file.write(f'num_roles = {nRoles};\n')


        file.write("availability = [\n" + "\n".join(
            ["    {" + ", ".join(map(str, sorted(row))) + "}," for row in availability]
        ) + "\n];\n")
        file.write("\n")

        # Write the array
        file.write(f"roles = [{', '.join(map(str, rolePeople))}];\n")


def runModel():
    model = Model("./JEEC.mzn")
    solver = Solver.lookup("gecode")
    instance = Instance(solver, model)
    instance.add_file("./JEECdata.dzn")

    result = instance.solve(timeout=timedelta(seconds=60))
    
    return result


def main():
    availability, roles, nShifts = Read_file_json()
    write_output_file("JEECdata.dzn", len(roles), nShifts, 20, 7, roles, availability)
    result = runModel()

    if result is None:
        print("No feasible solution found!")
        return

    assigned = np.array(result["assigned"])


    # Print assignments
    for i in range(assigned.shape[0]):
        shifts = [j + 1 for j in range(assigned.shape[1]) if assigned[i][j] == 1]
        print(f"Person {i}: {shifts} - #Shifts = {len(shifts)}")

main()