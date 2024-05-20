var currentSvgIndex = 0;
var svgArray = []; // This is a large array containing all SVGs

$(document).ready(
    function() 
    {
        // Variables to track the initial click position and shooting strength
        var initialClickX, initialClickY;
        var shootingDirectionLine;
        var shotInProgress = false;

        initializeCueBall();

        function initializeCueBall() {
            console.log("initialized cue...")
            $(document).on('mousemove', handleMouseMove);

            $('#0').on('mousedown', function(event) {
                if (!shotInProgress) {
                    ballHandle(event);
                }
            });
        }

        function ballHandle(event){
            $(document).off('mousemove', handleMouseMove);
                // Store the initial click position
                initialClickX = event.pageX;
                initialClickY = event.pageY;
                // Call the pullback function
                pullback();
                // Start tracking mouse movement
                $(document).on('mousemove', handleMouseMoveForPullBack);
                $(document).on('mouseup', shoot)
        }

        function pullback(event) {
            // Start tracking mouse movement
            $(document).on('mousemove', handleMouseMoveForPullBack);
        }

        function shoot() {
            // Stop tracking mouse movement
            $(document).off('mousemove', handleMouseMoveForPullBack);

            // Call the shoot function
            handleShoot();
            
            $(document).on('mousemove', handleMouseMove);

            // Remove mouse up event listener
            $(document).off('mouseup', shoot);

            updateShootingDirectionLine(0, 0, 0, 0, 0);

        }

        function updateSVG() {
            $.get('/pool.html', function(data) {
            $('#pool-table').html(data);
            });
        }

    // Function to track mouse movement
        function handleMouseMove(event) {
            // Get the position of the SVG canvas
            var svgOffset = $('#pool-table').offset();

            // Calculate the scaling factor based on the viewBox parameters
            var viewBoxParams = $('#pool-table')[0].viewBox.baseVal;
            var scaleX = viewBoxParams.width / $('#pool-table').width();
            var scaleY = viewBoxParams.height / $('#pool-table').height();

            // Calculate the cue ball's position relative to the SVG canvas
            var cueBallPos = calculateOffset(event, svgOffset, viewBoxParams, scaleX, scaleY);

            // Update coordinates display
            $('#x-coord').text(cueBallPos.x);
            $('#y-coord').text(cueBallPos.y);

            // Update cue ball position
            //var cueBall = $('#0');
            //cueBall.attr('cx', cueBallPos.x);
            //cueBall.attr('cy', cueBallPos.y);
        }

        // Function to calculate cue ball position
        function calculateOffset(event, svgOffset, viewBoxParams, scaleX, scaleY) {
            // Calculate the cue ball's position relative to the SVG canvas
            var cueBallX = (event.pageX - svgOffset.left) * scaleX + viewBoxParams.x;
            var cueBallY = (event.pageY - svgOffset.top) * scaleY + viewBoxParams.y;

            // Ensure the cue ball stays within the boundaries of the pool table
            var leftBoundary = viewBoxParams.x;
            var topBoundary = viewBoxParams.y;
            var rightBoundary = viewBoxParams.x + viewBoxParams.width;
            var bottomBoundary = viewBoxParams.y + viewBoxParams.height;

            newX = Math.min(Math.max(cueBallX, leftBoundary), rightBoundary);
            newY = Math.min(Math.max(cueBallY, topBoundary), bottomBoundary);

            return { x: newX, y: newY };
        }


        // Function to handle mouse move event for pull back
        function handleMouseMoveForPullBack(event) {
            
            var svgOffset = $('#pool-table').offset();

            // Calculate the scaling factor based on the viewBox parameters
            var viewBoxParams = $('#pool-table')[0].viewBox.baseVal;
            var scaleX = viewBoxParams.width / $('#pool-table').width();
            var scaleY = viewBoxParams.height / $('#pool-table').height();

            var endPos = calculateOffset(event, svgOffset, viewBoxParams, scaleX, scaleY);

            // Calculate the distance moved from the initial click position
            var deltaX = event.pageX - initialClickX;
            var deltaY = event.pageY - initialClickY;

            //var newX = ('#0').attr('cx') + deltaX
            //var newY = ('#0').attr('cy') + deltaY

            // Calculate the shooting strength based on the distance moved
            shootingStrength = Math.sqrt(deltaX * deltaX + deltaY * deltaY);

            updateShootingDirectionLine($('#0').attr('cx'), $('#0').attr('cy'), endPos.x, endPos.y, 10);


            // Update the display with shooting strength (you can customize this according to your UI)
            $('#shooting-strength').text('Shooting Strength: ' + Math.round(shootingStrength));

        }

        function updateShootingDirectionLine(startX, startY, endX, endY, width) 
        {
            var cueBallOffsetX = parseFloat($('#0').attr('cx'));
            var cueBallOffsetY = parseFloat($('#0').attr('cy'));

            // Create the SVG line element if it doesn't exist
            var shootingDirectionLine = $('#shooting-direction-line');

            shootingDirectionLine.attr({
                'x1': startX,
                'y1': startY,
                'x2': endX,
                'y2': endY,
                'stroke-width': width
            });

            // Append the line to the SVG container

        }
        // Function to handle mouse up event to shoot the cue ball
        function handleShoot() {
            var releaseX = event.pageX;
            var releaseY = event.pageY;
            var cueBall = $('#0');
            var cueBallX = parseInt(cueBall.attr('cx'));
            var cueBallY = parseInt(cueBall.attr('cy'));
            var velocityX = (releaseX - cueBallX);
            var velocityY = (releaseY - cueBallY);
    
            shotInProgress = true;
    
            shootCueBall(velocityX, velocityY);
        }
        // Function to shoot the cue ball
        function shootCueBall(initialXVelocity, initialYVelocity) 
        {
            console.log("Shooting cue ball with velocity:", initialXVelocity, initialYVelocity);

            sendDataToServer(initialXVelocity, initialYVelocity)

            //setTimeout(function() {
            shotInProgress = false;
            initializeCueBall(); 
            //}, 10000); // Assuming the shoot animation takes 2 seconds
        }

        function sendDataToServer(initialXVelocity, initialYVelocity) {
            // Create an object containing the data to send
            console.log("Sending data to server...");
            // Create an object containing the data to send
            var data = {
                velocityX: initialXVelocity,
                velocityY: initialYVelocity,
            };    

            $.ajax({
                type: "POST",
                url: "/trigger_shoot",
                data: JSON.stringify(data), // Your shoot action data
                contentType: "application/json",
                success: function(response) {
                    getUpdatedSvg();
                    console.log("Hey there 1");
                    // Upon successful shoot action, make AJAX request to '/get_updated_svg' endpoint
                },
                error: function(xhr, status, error) {
                    console.error("Error:", error);
                }
            });
          }
        
        function getUpdatedSvg() {
            $.ajax({
                type: "GET",
                url: "/get_updated_svg",
                success: function(response) {
                    //console.log(response.svg_contents); 
                    // Update SVG contents in HTML dynamically

                    updateSvgContents(response.svg_contents);
                },
                error: function(xhr, status, error) {
                    console.error("Error:", error);
                }
            });
        }

        function updateSvgContents(svgContents) {
            // Assuming there is a div with id "svg-container" where you want to append or replace SVGs
            var svgContainer = document.getElementById("pool-table-container");
            
            // Clear the existing contents of the SVG container
            svgContainer.innerHTML = "";
        
            // Display each SVG one at a time with a delay between each display
            for (var i = 0; i < svgContents.length; i++) {
                // Create a closure to capture the current value of 'i'
                (function(index) {
                    setTimeout(function() {
                        // Set the innerHTML of the SVG container to the SVG at the current index
                        svgContainer.innerHTML = svgContents[index];
                    }, i * 10); // Change 1000 to the desired delay between each SVG display in milliseconds
                })(i);
            }

        }
        
        handleMouseMove({ pageX: 0, pageY: 0 })
        console.log("finished")

  });

        