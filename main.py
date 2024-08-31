
function love.load()
    love.window.setTitle("Simple Soccer Game")
    love.window.setMode(800, 600)

    paddleWidth, paddleHeight = 20, 100
    leftPaddle = {x = 30, y = 250, speed = 300}
    rightPaddle = {x = 750, y = 250, speed = 300}

    ball = {x = 400, y = 300, size = 20, speedX = 200, speedY = 150}

    score = {left = 0, right = 0}
end

function love.update(dt)
    if love.keyboard.isDown("w") then
        leftPaddle.y = math.max(0, leftPaddle.y - leftPaddle.speed * dt)
    elseif love.keyboard.isDown("s") then
        leftPaddle.y = math.min(600 - paddleHeight, leftPaddle.y + leftPaddle.speed * dt)
    end

    if love.keyboard.isDown("up") then
        rightPaddle.y = math.max(0, rightPaddle.y - rightPaddle.speed * dt)
    elseif love.keyboard.isDown("down") then
        rightPaddle.y = math.min(600 - paddleHeight, rightPaddle.y + rightPaddle.speed * dt)
    end


    ball.x = ball.x + ball.speedX * dt
    ball.y = ball.y + ball.speedY * dt


    if ball.y <= 0 or ball.y >= 600 - ball.size then
        ball.speedY = -ball.speedY
    end


    if checkCollision(ball, leftPaddle) then
        ball.speedX = -ball.speedX
        ball.x = leftPaddle.x + paddleWidth
    elseif checkCollision(ball, rightPaddle) then
        ball.speedX = -ball.speedX
        ball.x = rightPaddle.x - ball.size
    end


    if ball.x < 0 then
        score.right = score.right + 1
        resetBall()
    elseif ball.x > 800 - ball.size then
        score.left = score.left + 1
        resetBall()
    end
end


function love.draw()

    love.graphics.rectangle("fill", leftPaddle.x, leftPaddle.y, paddleWidth, paddleHeight)
    love.graphics.rectangle("fill", rightPaddle.x, rightPaddle.y, paddleWidth, paddleHeight)


    love.graphics.rectangle("fill", ball.x, ball.y, ball.size, ball.size)

    love.graphics.print("Score: " .. score.left, 200, 20)
    love.graphics.print("Score: " .. score.right, 600, 20)
end

function checkCollision(ball, paddle)
    return ball.x < paddle.x + paddleWidth and
           ball.x + ball.size > paddle.x and
           ball.y < paddle.y + paddleHeight and
           ball.y + ball.size > paddle.y
end

function resetBall()
    ball.x, ball.y = 400, 300
    ball.speedX = -ball.speedX
end

