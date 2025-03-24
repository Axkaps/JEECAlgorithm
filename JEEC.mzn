int: num_people;
int: num_shifts;
int: max_people_per_shift;
int: num_roles;

% Role of each person (1..num_roles)
array[1..num_people] of int: roles;
% Available shifts for each person
array[1..num_people] of set of int: availability;

% Decision variable: assigned[i,j] = 1 if person i is assigned to shift j
array[1..num_people, 1..num_shifts] of var 0..1: assigned;

% 1. Ensure people are only assigned to available shifts
constraint forall(i in 1..num_people, j in availability[i]) (
    assigned[i, j] = 1
);


% 2. Calculate workload per person
array[1..num_people] of var int: workload;
constraint forall(i in 1..num_people) (
    workload[i] = sum(j in 1..num_shifts) (assigned[i, j])
);

% 3. Limit people per shift
constraint forall(j in 1..num_shifts) (
    sum(i in 1..num_people) (assigned[i, j]) <= max_people_per_shift
);

% 4. Ensure at least one person per role per shift
constraint forall(j in 1..num_shifts, r in 1..num_roles) (
    exists(i in 1..num_people where roles[i] == r) (assigned[i, j] == 1)
);

% 5. Minimize workload imbalance
var int: min_workload = min(workload);
var int: max_workload = max(workload);
var int: deviation = max_workload - min_workload;

solve minimize deviation;
