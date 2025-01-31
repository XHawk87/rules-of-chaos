-- Place Ruins at the location of the destroyed city.
function CityDestroyedCallback(city, loser, destroyer)
    city.tile:create_extra("Ruins", NIL)
    -- continue processing
    return false
end

signal.connect("city_destroyed", "CityDestroyedCallback")
