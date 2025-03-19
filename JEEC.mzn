int: num_people;        % Number of people
int: num_shifts;        % Number of shifts
int: max_people_per_shift; % Max people per shift
int: num_roles;         % Number of different roles

array[1..num_people, 1..num_shifts] of var 0..1: assigned; % Decision variable
array[1..num_people] of int: roles; % The role of each person (1, 2, 3, ...)

array[1..num_people, 1..num_shifts] of int: availability; % Availability matrix

% A person can only work a shift if they are available
constraint forall(i in 1..num_people, j in 1..num_shifts) (
    assigned[i, j] <= availability[i, j]
);

% Each shift has a max number of assigned people
constraint forall(j in 1..num_shifts) (
    sum(i in 1..num_people) assigned[i, j] <= max_people_per_shift
);

array[1..num_roles, 1..num_shifts] of var 0..max_people_per_shift: role_count;

% Count the number of people in each role per shift
constraint forall(r in 1..num_roles, j in 1..num_shifts) (
    role_count[r, j] = sum(i in 1..num_people where roles[i] = r) assigned[i, j]
);

% Ensure each shift has exactly 2 people of the same role
constraint forall(j in 1..num_shifts) (
    exists(r in 1..num_roles) (role_count[r, j] = 2)
);

array[1..num_people] of var int: workload; % Number of shifts per person

% Calculate the workload for each person
constraint forall(i in 1..num_people) (
    workload[i] = sum(j in 1..num_shifts) assigned[i, j]
);

var int: min_workload = min(workload);
var int: max_workload = max(workload);
var int: deviation = max_workload - min_workload;

solve minimize deviation; % Minimize workload imbalance