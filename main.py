function love.load()
    love.window.setTitle("Advanced Soccer Game")
    love.window.setMode(800, 600)

    paddleWidth, paddleHeight = 20, 100
    leftPaddle = {x = 30, y = 250, speed = 300}
    rightPaddle = {x = 750, y = 250, speed = 250}

    ball = {x = 400, y = 300, size = 20, speedX = 200, speedY = 150, speedMultiplier = 1.05}

    score = {left = 0, right = 0}
    winningScore = 5
    gameActive = true
end

function love.update(dt)
    if gameActive then
        if love.keyboard.isDown("w") then
            leftPaddle.y = math.max(0, leftPaddle.y - leftPaddle.speed * dt)
        elseif love.keyboard.isDown("s") then
            leftPaddle.y = math.min(600 - paddleHeight, leftPaddle.y + leftPaddle.speed * dt)
        end

        aiMove(dt)

        ball.x = ball.x + ball.speedX * dt
        ball.y = ball.y + ball.speedY * dt

        if ball.y <= 0 or ball.y >= 600 - ball.size then
            ball.speedY = -ball.speedY
        end

        if checkCollision(ball, leftPaddle) then
            ball.speedX = -ball.speedX * ball.speedMultiplier
            adjustBallAngle(ball, leftPaddle)
        elseif checkCollision(ball, rightPaddle) then
            ball.speedX = -ball.speedX * ball.speedMultiplier
            adjustBallAngle(ball, rightPaddle)
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
    else
        if love.keyboard.isDown("space") then
            resetGame()
        end
    end
end

function love.draw()
    drawCourt()
    love.graphics.rectangle("fill", leftPaddle.x, leftPaddle.y, paddleWidth, paddleHeight)
    love.graphics.rectangle("fill", rightPaddle.x, rightPaddle.y, paddleWidth, paddleHeight)
    love.graphics.rectangle("fill", ball.x, ball.y, ball.size, ball.size)

    love.graphics.print("Score: " .. score.left, 200, 20)
    love.graphics.print("Score: " .. score.right, 600, 20)

    if not gameActive then
        love.graphics.printf("Player " .. (score.left >= winningScore and "Left" or "Right") .. " Wins!\nPress Space to Restart", 0, 250, 800, "center")
    end
end

function checkCollision(ball, paddle)
    return ball.x < paddle.x + paddleWidth and
           ball.x + ball.size > paddle.x and
           ball.y < paddle.y + paddleHeight and
           ball.y + ball.size > paddle.y
end

function resetBall()
    ball.x, ball.y = 400, 300
    ball.speedX = -ball.speedX * 0.8
    ball.speedY = 150 * (ball.speedY > 0 and 1 or -1)
end

function aiMove(dt)
    if ball.y + ball.size / 2 > rightPaddle.y + paddleHeight / 2 then
        rightPaddle.y = math.min(600 - paddleHeight, rightPaddle.y + rightPaddle.speed * dt)
    else
        rightPaddle.y = math.max(0, rightPaddle.y - rightPaddle.speed * dt)
    end
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

function resetGame()
    score.left, score.right = 0, 0
    gameActive = true
    resetBall()
end

function drawCourt()
    love.graphics.setLineWidth(4)
    love.graphics.line(400, 0, 400, 600)
    love.graphics.rectangle("line", 0, 0, 800, 600)
    love.graphics.rectangle("line", 0, 200, 20, 200)
    love.graphics.rectangle("line", 780, 200, 20, 200)
end
