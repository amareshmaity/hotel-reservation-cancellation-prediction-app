from scipy.stats import randint, uniform

# LIGHTGM_PARAMS = {
#     "n_estimators": randint(100,500),
#     "max_depth": randint(5,50),
#     "learning_rate": uniform(0.01,0.2),
#     "num_leaves": randint(20,100),
#     "boosting_type": ['gbdt', 'dart', 'goss']
# }


# RANDOM_SEARCH_PARAMS = {
#     "n_iter": 4,
#     "cv": 2,
#     "n_jobs": -1,
#     "verbose": 2,
#     "random_state": 42,
#     "scoring": "accuracy"
# }

## Update params for faster training during jenkins build

LIGHTGM_PARAMS = {
    "n_estimators": randint(50, 150),         # Lower limits for faster CI/CD testing
    "max_depth": randint(3, 10),              # Deep trees (up to 50) blow up memory
    "learning_rate": uniform(0.05, 0.2),
    "num_leaves": randint(20, 50),            # Restrict leaf nodes to prevent long builds
    "boosting_type": ['gbdt', 'goss'],        # REMOVED 'dart' to eliminate the slowdown
    "verbose": [-1]                           # <-- CRUCIAL: Mutes the endless log loop
}

RANDOM_SEARCH_PARAMS = {
    "n_iter": 3,                              # 3 iterations is plenty to verify the pipeline
    "cv": 2,
    "n_jobs": 1,                              # <-- CRUCIAL: Set to 1 to prevent Docker process locking
    "verbose": 0,                             # Mutes Scikit-Learn search text tracking
    "random_state": 42,
    "scoring": "accuracy"
}
