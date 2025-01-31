-- Initialise global namespace for portal data
InvisiblePortals = {
    traversing = {}
}

function InvisiblePortals:log(level, fmt, ...)
    log.base(level, string.format("Invisible Portals: " .. fmt, ...))
end

function InvisiblePortals:debug(fmt, ...)
    self:log(log.level.DEBUG, "[DEBUG] " .. fmt, ...)
end

function InvisiblePortals:info(fmt, ...)
    self:log(log.level.NORMAL, "[INFO] " .. fmt, ...)
end

function InvisiblePortals:portal_count()
    local count = 0
    for _ in pairs(self.portals) do
        count = count + 1
    end
    return count
end

function InvisiblePortals:serialise_portals()
    local portals = {}
    for source_id, dest_id in pairs(self.portals) do
        table.insert(portals, source_id .. "=" .. dest_id)
    end
    return table.concat(portals, ",")
end

function InvisiblePortals:init()
    self:debug("Creating namespace")
    local half_life = features.invisiblePortals.halfLife
    local density = features.invisiblePortals.density
    local collapse_chance = 1 - 2 ^ (-1 / half_life)
    local form_chance = (density * collapse_chance) / (1 - density)
    self.initial_density_freq = math.floor(density * 1000000)
    self.initial_density_range = 1000000
    self:info("Initial portal density = %d / %d",
        self.initial_density_freq, self.initial_density_range)
    self.collapse_chance_freq = math.floor(collapse_chance * 1000000)
    self.collapse_chance_range = 1000000
    self:info("Portal collapse chance per turn = %d / %d",
        self.collapse_chance_freq, self.collapse_chance_range)
    self.form_chance_freq = math.floor(form_chance * 1000000)
    self.form_chance_range = 1000000
    self:info("Portal form chance per turn = %d / %d",
        self.form_chance_freq, self.form_chance_range)
    local _portal_cache = NIL
    setmetatable(self, {
        __index = function(_, key)
            if key == "portals" then
                if not _portal_cache then
                    _portal_cache = {}
                    self:load_portals()
                end
                return _portal_cache
            end
        end
    })
    self:debug("Namespace created")
end

function InvisiblePortals:save_portals()
    self:debug("Saving portals")
    InvisiblePortals_data = self:serialise_portals()
    self:info("%d portals saved", self:portal_count())
    self:debug("invisible_portals_data = %s", InvisiblePortals_data)
    self:debug("Portal save complete")
end

function InvisiblePortals:load_portals()
    self:debug("Loading portals")
    if not InvisiblePortals_data then
        self:debug("No previous portal data found")
        return
    end
    -- If the map has already been generated, count the map tiles
    InvisiblePortals:count_map_tiles()
    for source_id, dest_id in string.gmatch(InvisiblePortals_data, "(%w+)=(%w+)") do
        self:create_portal(source_id, dest_id)
    end
    self:info("%d portals loaded", self:portal_count())
    self:debug("Portal data loaded from save: %s", InvisiblePortals_data)
end

-- Count the number of tiles in the map after map generation
function InvisiblePortals:count_map_tiles()
    self:debug("Counting map tiles")
    local tile_count = 0
    for _ in whole_map_iterate() do
        tile_count = tile_count + 1
    end
    self.tile_count = tile_count
    self:info("%d map tiles detected", self.tile_count)
end

-- Create a new portal on a tile with a random destination
function InvisiblePortals:create_random_portal(tile)
    self:debug("Creating a new portal at %s", tile)
    local dest_id = random(0, self.tile_count - 1)
    self.portals[tile.id] = dest_id
    local dest_tile = find.tile(dest_id)
    self:info("A new portal formed at (%d, %d) leading to (%d, %d)",
        tile.x, tile.y, dest_tile.x, dest_tile.y)
end

-- Create a portal on a tile with a specific destination
function InvisiblePortals:create_portal(source_id, dest_id)
    self:debug("Creating a portal at %s to %s", source_id, dest_id)
    self.portals[tonumber(source_id)] = tonumber(dest_id)
    local source_tile = find.tile(source_id)
    local dest_tile = find.tile(dest_id)
    self:info("A portal opened at (%d, %d) leading to (%d, %d)",
        source_tile.x, source_tile.y, dest_tile.x, dest_tile.y)
end

-- Remove a portal
function InvisiblePortals:destroy_portal(tile_id)
    self:debug("Destroying portal #%s", tile_id)
    local tile = find.tile(tile_id)
    local dest_id = self.portals[tile_id]
    self.portals[tile_id] = NIL
    local dest_tile = find.tile(dest_id)
    self:info("Portal at (%d, %d) leading to (%d, %d) collapsed",
        tile.x, tile.y, dest_tile.x, dest_tile.y)
end

-- Distribute initial portals across the map
function InvisiblePortals:create_initial_portals()
    self:info("Creating initial portals")
    local range = self.initial_density_range
    local freq = self.initial_density_freq
    for tile in whole_map_iterate() do
        if random(0, range) < freq then
            self:create_random_portal(tile)
        end
    end
    self:info("Initial portals created")
    self:save_portals()
end

-- New portals form over time
function InvisiblePortals:create_new_portals()
    self:info("New portals forming")
    local range = self.form_chance_range
    local freq = self.form_chance_freq
    for tile in whole_map_iterate() do
        local destination = self.portals[tile.id]
        if not destination and random(0, range) < freq then
            self:create_random_portal(tile)
        end
    end
    self:info("Done forming new portals")
end

-- Existing portals have a chance to collapse each turn
function InvisiblePortals:expire_old_portals()
    self:info("Expiring old portals")
    local range = self.collapse_chance_range
    local freq = self.collapse_chance_freq
    for source_id in pairs(self.portals) do
        if random(0, range) < freq then
            self:destroy_portal(source_id)
        end
    end
    self:info("Done expiring old portals")
end

function InvisiblePortals:disembark_at_portal(unit, source_tile)
    for cargo in unit:cargo_iterate() do
        self:info("%s %s was forced to disembark from %s %s during portal transit",
            cargo, cargo.utype:name_translation(),
            unit, unit.utype:name_translation()
        )
        self:traverse_portal(cargo, source_tile, source_tile)
    end
end

function InvisiblePortals:fatal_transit_allowed(player)
    if player:has_flag("ai") then
        return features.invisiblePortals.allowFatalTransitAI
    else
        return features.invisiblePortals.allowFatalTransit
    end
end

function InvisiblePortals:traverse_portal(unit, src_tile, dst_tile)
    self:debug("Unit %s moved from (%d, %d) to (%d, %d)",
        unit, src_tile.x, src_tile.y, dst_tile.x, dst_tile.y)
    local dest_id = self.portals[dst_tile.id]
    if not dest_id then return end
    local unit_id = unit.id
    if self.traversing[unit_id] then
        return -- Units can't traverse two portals at once
    end
    local destination = find.tile(dest_id)
    local owner = unit.owner
    local fatal = self:fatal_transit_allowed(owner)
    local unit_string = tostring(unit)
    local unit_tag = unit.utype:name_translation()
    -- Fix for https://github.com/longturn/freeciv21/issues/2475
    local survived
    if not unit.utype:can_exist_at_tile(destination) then
        self:disembark_at_portal(unit, dst_tile)
        if fatal then
            unit:kill("nonnative_terr", NIL)
            survived = false
        else
            return
        end
    elseif destination:is_enemy(owner) then
        if fatal then
            unit:kill("killed", NIL)
            survived = false
        else
            return
        end
    else
        self.traversing[unit_id] = true
        survived = unit:teleport(destination)
        self.traversing[unit_id] = NIL
    end
    local outcome_text = survived
        and string.format(
            "reappearing some distance away at (%d, %d)",
            destination.x, destination.y
        )
        or "never to be seen again"
    local message = string.format(
        "Your %s has fallen through a tear in space at (%d, %d), %s.",
        unit_tag, dst_tile.x, dst_tile.y, outcome_text
    )
    notify.event(owner, destination, E.SCRIPT, message)
    self:info("%s %s took portal from (%d, %d) to (%d, %d) and %s",
        unit_string, unit_tag, dst_tile.x, dst_tile.y, destination.x, destination.y,
        survived and "survived" or "died")
end

-- Initialise portals at map creation
function InvisiblePortals_initialisePortalsOnMapGen()
    InvisiblePortals:debug("Starting post-mapgen actions")
    InvisiblePortals:count_map_tiles()
    InvisiblePortals:create_initial_portals()
    InvisiblePortals:debug("Finished post-mapgen actions")
end

-- Expire old portals and create new portals at turn start
function InvisiblePortals_updatePortalsAtTurnStart()
    InvisiblePortals:debug("Starting post-TC actions")
    InvisiblePortals:expire_old_portals()
    InvisiblePortals:create_new_portals()
    InvisiblePortals:save_portals()
    InvisiblePortals:debug("Finished post-TC actions")
end

-- When a unit lands on a portal, it teleports to the destination
function InvisiblePortals_traversePortalOnEnter(unit, src_tile, dst_tile)
    InvisiblePortals:debug("Starting post-unit-move actions")
    InvisiblePortals:traverse_portal(unit, src_tile, dst_tile)
    InvisiblePortals:debug("Finished post-unit-move actions")
end

InvisiblePortals:info("Initialising...")
InvisiblePortals:init()
signal.connect("map_generated", "InvisiblePortals_initialisePortalsOnMapGen")
signal.connect("turn_begin", "InvisiblePortals_updatePortalsAtTurnStart")
signal.connect("unit_moved", "InvisiblePortals_traversePortalOnEnter")
InvisiblePortals:info("Initialisation complete")
