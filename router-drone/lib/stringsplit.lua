-- @author Alex Carrillo
--

function split(input_str, delimiter) do
    if _VERSION=="Lua 5.0.2" then
        matcher = string.gfind
    else
        matcher = string.gmatch
    end
    tab = {}
    i = 0
    for str in matcher(input_str, "([^"..delimiter.."]+)") do
        tab[i] = str
        i=i+1
    end
    return tab
end
end
