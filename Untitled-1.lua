local creator = game:GetService("MarketplaceService"):GetProductInfo(game.PlaceId).Creator.CreatorTargetId
coroutine.wrap(function()
if game.PlaceId == 10449761463 then --- TSB
loadstring(game:HttpGet("https://api.luarmor.net/files/v3/loaders/1ac9b54586a547470e1dd3bdc77ee94c.lua"))()

elseif game.PlaceId == 891852901 then --- GreenVille
loadstring(game:HttpGet("https://api.luarmor.net/files/v3/loaders/832543db68401da3a175248c3869edf5.lua"))()

elseif game:GetService("ReplicatedStorage"):FindFirstChild("Packages") and game:GetService("ReplicatedStorage").Packages:FindFirstChild("Knit") and game:GetService("ReplicatedStorage").Packages.Knit:FindFirstChild("Services") and game:GetService("ReplicatedStorage").Packages.Knit.Services:FindFirstChild("BallService") then
loadstring(game:HttpGet("https://api.luarmor.net/files/v3/loaders/d6096bf59db7fea1dd9bb3ecab113289.lua"))()


elseif game.PlaceId == 15092647980 or game.PlaceId == 16200303170 then --- Project Smash
loadstring(game:HttpGet("https://api.luarmor.net/files/v3/loaders/e453d35c652dc59f67581353bc5a6650.lua"))()

elseif game.PlaceId == 2534724415 then --- Emergency Response: Liberty County

coroutine.wrap(function()
pcall(function()
local original1 = getgenv().printconsole or function() return end
local original2 = getgenv().print or function() return end
getgenv().printconsole = function() return end
getgenv().print = function() return end
wait(30)
getgenv().printconsole = original1
getgenv().print = original2
end)
end)()

loadstring(game:HttpGet("https://api.luarmor.net/files/v3/loaders/d8afdb07fbbcee024e2d22bfeab6abbd.lua"))()

elseif game.PlaceId == 537413528 then --- Build A Boat For Treasure
loadstring(game:HttpGet("https://api.luarmor.net/files/v3/loaders/bce5241ec70323b994da2a7fa9e75901.lua"))()
      
elseif game.PlaceId == 3351674303 then --diving empire
loadstring(game:HttpGet("https://api.luarmor.net/files/v3/loaders/1fdc5e92eec9c5b02c8635df4f365a75.lua"))()

elseif game.PlaceId == 13621938427 then --untitled boxing
loadstring(game:HttpGet("https://api.luarmor.net/files/v3/loaders/c4fe1e0b584949739e7c98ea98e0180b.lua"))()

elseif creator == 11867394 then --dead rails
loadstring(game:HttpGet("https://api.luarmor.net/files/v3/loaders/049986471e716d7e1960bb897309b8f1.lua"))()

elseif game.PlaceId == 6520999642 then --basically fnf
getgenv().fnfcmb = true
loadstring(game:HttpGet("https://api.luarmor.net/files/v3/loaders/d44b4ce46a7c1edbf18ad513122feaee.lua"))()
end
end)()

pcall(function()
if game.Players.LocalPlayer.PlayerGui:FindFirstChild("TouchGui") then
local a=Instance.new("ScreenGui",game.CoreGui)a.Name="ElysiumLogo"a.ZIndexBehavior=Enum.ZIndexBehavior.Sibling;local b=Instance.new("ImageButton")b.Name="ElysiumButton"b.Size=UDim2.new(0,116,0,105)b.Visible=true;b.BorderColor3=Color3.fromRGB(0,0,0)b.BackgroundTransparency=1;b.Position=UDim2.new(0.1252033,0,0.6278195,0)b.BorderSizePixel=0;b.BackgroundColor3=Color3.fromRGB(255,255,255)b.Image="http://www.roblox.com/asset/?id=127256367572086"b.Parent=a;local c=game.CoreGui;local d=c:WaitForChild("toui;lib")local function e()d.Enabled=not d.Enabled end;local f=game:GetService("UserInputService")f.InputBegan:Connect(function(g)if g.UserInputType==Enum.UserInputType.Touch then b.Position=UDim2.new(0.5,-58,0.5,-52.5)end end)b.MouseButton1Click:Connect(e)local h=false;local i,j,k;local function l(g)local m=g.Position-j;b.Position=UDim2.new(k.X.Scale,k.X.Offset+m.X,k.Y.Scale,k.Y.Offset+m.Y)end;b.InputBegan:Connect(function(g)if g.UserInputType==Enum.UserInputType.MouseButton1 or g.UserInputType==Enum.UserInputType.Touch then h=true;j=g.Position;k=b.Position;g.Changed:Connect(function()if g.UserInputState==Enum.UserInputState.End then h=false end end)end end)b.InputChanged:Connect(function(g)if g.UserInputType==Enum.UserInputType.MouseMovement or g.UserInputType==Enum.UserInputType.Touch then i=g end end)game:GetService("UserInputService").InputChanged:Connect(function(g)if g==i and h then l(g)end end)
end
end)