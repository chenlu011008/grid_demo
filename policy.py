def move_towards_goal(agent):
    """
    Simple deterministic movement towards goal.
    Prioritize x movement first, then y.
    """
    x, y = agent.pos
    gx, gy = agent.goals[agent.current_goal_idx]

    if x < gx:
        return (1, 0)
    elif x > gx:
        return (-1, 0)
    elif y < gy:
        return (0, 1)
    elif y > gy:
        return (0, -1)
    else:
        return (0, 0)
    
