function love.load()
    love.window.setTitle("Advanced Soccer Game")
    love.window.setMode(800, 600)

    paddleWidth, paddleHeight = 20, 100
    leftPaddle = {x = 30, y = 250, speed = 300, boost = 1.5}
    rightPaddle = {x = 750, y = 250, speed = 250, difficulty = 1}

    ball = {x = 400, y = 300, size = 20, speedX = 200, speedY = 150, speedMultiplier = 1.05}

    score = {left = 0, right = 0}
    winningScore = 5
    gameActive = false
    paused = false
    playerNameLeft = ""
    playerNameRight = "AI"
    inputActive = true
    inputField = ""

    powerUps = {}
    powerUpSpawnTimer = 5
    powerUpEffectDuration = 3

    particles = {}
end

function love.update(dt)
    if gameActive and not paused then
        updatePaddleMovement(dt)
        aiMove(dt)
        updateBallMovement(dt)
        updatePowerUps(dt)
        updateParticles(dt)
        checkCollisions()
    end

    if inputActive then
        if love.keyboard.isDown("return") and inputField ~= "" then
            if playerNameLeft == "" then
                playerNameLeft = inputField
                inputField = ""
            elseif playerNameRight == "AI" then
                playerNameRight = inputField ~= "" and inputField or "AI"
                inputActive = false
                gameActive = true
            end
        elseif love.keyboard.isDown("backspace") and #inputField > 0 then
            inputField = inputField:sub(1, -2)
        end
    end

    if love.keyboard.isDown("p") and not inputActive then
        paused = not paused
    end
end

function love.draw()
    love.graphics.setBackgroundColor(0.1, 0.1, 0.1)
    drawCourt()
    drawPaddles()
    drawBall()
    drawScore()
    drawPowerUps()
    drawParticles()

    if paused then
        love.graphics.printf("Paused\nPress 'P' to Resume", 0, 250, 800, "center")
    elseif inputActive then
        drawInputScreen()
    elseif not gameActive then
        love.graphics.printf("Player " .. (score.left >= winningScore and playerNameLeft or playerNameRight) .. " Wins!\nPress Space to Restart", 0, 250, 800, "center")
    end
end

function updatePaddleMovement(dt)
    if love.keyboard.isDown("w") then
        leftPaddle.y = math.max(0, leftPaddle.y - leftPaddle.speed * dt * (love.keyboard.isDown("lshift") and leftPaddle.boost or 1))
    elseif love.keyboard.isDown("s") then
        leftPaddle.y = math.min(600 - paddleHeight, leftPaddle.y + leftPaddle.speed * dt * (love.keyboard.isDown("lshift") and leftPaddle.boost or 1))
    end
end

function aiMove(dt)
    if rightPaddle.difficulty == 1 then
        targetY = ball.y + ball.size / 2
    elseif rightPaddle.difficulty == 2 then
        targetY = ball.y
    else
        targetY = ball.y + ball.size / 2 * math.random(-1, 1)
    end

    if targetY > rightPaddle.y + paddleHeight / 2 then
        rightPaddle.y = math.min(600 - paddleHeight, rightPaddle.y + rightPaddle.speed * dt)
    else
        rightPaddle.y = math.max(0, rightPaddle.y - rightPaddle.speed * dt)
    end
end

function updateBallMovement(dt)
    ball.x = ball.x + ball.speedX * dt
    ball.y = ball.y + ball.speedY * dt

    if ball.y <= 0 or ball.y >= 600 - ball.size then
        ball.speedY = -ball.speedY
    end

    if ball.x < 0 then
        score.right = score.right + 1
        resetBall()
        checkWinningCondition()
    elseif ball.x > 800 - ball.size then
        score.left = score.left + 1
        resetBall()
        checkWinningCondition()
    end
end

function checkCollisions()
    if checkCollision(ball, leftPaddle) then
        ball.speedX = -ball.speedX * ball.speedMultiplier
        adjustBallAngle(ball, leftPaddle)
        createParticles(ball.x, ball.y)
    elseif checkCollision(ball, rightPaddle) then
        ball.speedX = -ball.speedX * ball.speedMultiplier
        adjustBallAngle(ball, rightPaddle)
        createParticles(ball.x, ball.y)
    end

    for i, powerUp in ipairs(powerUps) do
        if checkCollision(ball, powerUp) then
            ball.speedX = ball.speedX * 1.5
            ball.speedY = ball.speedY * 1.5
            table.remove(powerUps, i)
        end
    end
end

function updatePowerUps(dt)
    powerUpSpawnTimer = powerUpSpawnTimer - dt
    if powerUpSpawnTimer <= 0 then
        spawnPowerUp()
        powerUpSpawnTimer = 5 + math.random(0, 5)
    end
end

function spawnPowerUp()
    local powerUp = {x = math.random(200, 600), y = math.random(50, 550), size = 15}
    table.insert(powerUps, powerUp)
end

function drawPowerUps()
    love.graphics.setColor(0, 1, 0)
    for _, powerUp in ipairs(powerUps) do
        love.graphics.rectangle("fill", powerUp.x, powerUp.y, powerUp.size, powerUp.size)
    end
    love.graphics.setColor(1, 1, 1)
end

function createParticles(x, y)
    local particle = {x = x, y = y, size = 20, lifetime = 0.5}
    table.insert(particles, particle)
end

function updateParticles(dt)
    for i, particle in ipairs(particles) do
        particle.lifetime = particle.lifetime - dt
        if particle.lifetime <= 0 then
            table.remove(particles, i)
        end
    end
end

function drawParticles()
    love.graphics.setColor(1, 1, 0)
    for _, particle in ipairs(particles) do
        love.graphics.circle("fill", particle.x, particle.y, particle.size * particle.lifetime)
    end
    love.graphics.setColor(1, 1, 1)
end

function adjustBallAngle(ball, paddle)
    local relativeIntersectY = (paddle.y + paddleHeight / 2) - (ball.y + ball.size / 2)
    local normalizedRelativeIntersectionY = relativeIntersectY / (paddleHeight / 2)
    local bounceAngle = normalizedRelativeIntersectionY * math.pi / 4
    ball.speedY = -ball.speedX * math.sin(bounceAngle)
end

function checkWinningCondition()
    if score.left >= winningScore or score.right >= winningScore then
        gameActive = false
    end
end

function resetBall()
    ball.x, ball.y = 400, 300
    ball.speedX = -ball.speedX * 0.8
    ball.speedY = 150 * (ball.speedY > 0 and 1 or -1)
    createParticles(ball.x, ball.y)
end

function drawCourt()
    love.graphics.setLineWidth(4)
    love.graphics.setColor(1, 1, 1)
    love.graphics.line(400, 0, 400, 600)
    love.graphics.rectangle("line", 0, 0, 800, 600)
    love.graphics.setColor(0.8, 0.3, 0.3)
    love.graphics.rectangle("line", 0, 200, 20, 200)
    love.graphics.rectangle("line", 780, 200, 20, 200)
    love.graphics.setColor(1, 1, 1)
end

function drawPaddles()
    love.graphics.rectangle("fill", leftPaddle.x, leftPaddle.y, paddleWidth, paddleHeight)
    love.graphics.rectangle("fill", rightPaddle.x, rightPaddle.y, paddleWidth, paddleHeight)
end

function drawBall()
    love.graphics.rectangle("fill", ball.x, ball.y, ball.size, ball.size)
end

function drawScore()
    love.graphics.print(playerNameLeft .. ": " .. score.left, 200, 20)
    love.graphics.print(playerNameRight .. ": " .. score.right, 600, 20)
end

function drawInputScreen()
    love.graphics.printf("Enter Player Name:\n" .. inputField, 0, 250, 800, "center")
end

function checkCollision(a, b)
    return a.x < b.x + (b.size or paddleWidth) and
           a.x + a.size > b.x and
           a.y < b.y + (b.size or paddleHeight) and
           a.y + a.size > b.y
end
