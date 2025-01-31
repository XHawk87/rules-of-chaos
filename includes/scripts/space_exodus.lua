SpaceExodus = {}

function SpaceExodus:early_finish_bonus()
    local target_turn = features.spaceExodus.expectedLaunchTurn
    local turns_early = target_turn - game.current_turn()
    return turns_early * features.spaceExodus.earlyFinishMultiplier
end

function SpaceExodus:first_place_bonus(first)
    if first then
        return features.spaceExodus.firstPlaceBonus
    else
        return 0
    end
end

function SpaceExodus:score(player, first)
    local civ_score = player:civilization_score()
    local early_finish_bonus = self:early_finish_bonus()
    local first_place_bonus = self:first_place_bonus(first)
    local total_score = civ_score + early_finish_bonus + first_place_bonus
    log.normal("%s won a space exodus victory with %d civilization points, " ..
        "%d early finish points, and %d position bonus, for a total of %d",
        player,
        civ_score,
        early_finish_bonus,
        first_place_bonus,
        total_score
    )
    return total_score
end

function SpaceExodus:save_score(player, score)
    if (SpaceExodus_scores) then
        SpaceExodus_scores = SpaceExodus_scores .. ";"
    else
        SpaceExodus_scores = ""
    end
    SpaceExodus_scores = SpaceExodus_scores ..
        string.format("%d=%d", player.id, score)
end

function SpaceExodus:exodus(player)
    for unit in player:units_iterate() do
        unit:kill("disbanded")
    end
    for city in player:cities_iterate() do
        city:remove()
    end
end

function SpaceExodus:spaceship_launched(player, first)
    local score = self:score(player, first)
    notify.all(
        "%s has built a massive spaceship and departed in a great exodus, " ..
        "leaving only ruins behind. Final score: %d",
        player.name,
        score
    )
    self:save_score(player, score)
    self:exodus(player)
end

-- When a spaceship is launched, all units and cities leave the planet
function SpaceExodus_onAchievementGained(achievement, gainer, first)
    if achievement:rule_name() ~= "Spaceship Launch" then return end
    SpaceExodus:spaceship_launched(gainer, first)
end

signal.connect("achievement_gained", "SpaceExodus_onAchievementGained")
