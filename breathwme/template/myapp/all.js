function animateNextPhase() {
                if (!isAnimating) return;
                let currentDuration = durations[index] + "s";
                goldenLine.style.animation = "none";
                void goldenLine.offsetWidth;
  
                textElement.innerText = breathingTexts[shape][index];
                
                
                switch (shape) {
                    case "circle":
                        console.log(currentDuration);
                        div.style.width = "200px";
                        div.style.height = "200px";
                        div.style.borderRadius = "50%";
                        goldenLine.style.animation = `moveCircle ${currentDuration} linear 1`;
                        break;
                    case "square":
                        div.style.width = "200px";
                        div.style.height = "200px";
                        console.log(currentDuration);
                        goldenLine.style.animation = `moveSquare ${currentDuration} linear infinite`;
                        break;
                    case "hRectangle":
                        div.style.width = "300px";
                        div.style.height = "150px";
                        goldenLine.style.animation = `moveRectangleH ${currentDuration} linear 1`;
                        break;
                    case "vRectangle":
                        div.style.width = "150px";
                        div.style.height = "300px";
                        goldenLine.style.animation = `moveRectangleV ${currentDuration} linear 1`;
                        break;
                    case "triangle":
                        div.className = "triangle"; // Apply triangle styles
                        goldenLine.style.animation = `moveTriangle ${currentDuration} linear infinite`;
                         // Apply text styles only for the triangle case
                        textElement.style.position = "absolute";
                        textElement.style.color = "white";
                        textElement.style.fontSize = "20px";
                        textElement.style.zIndex = "2";
                        textElement.style.marginTop = "115px";
                        textElement.style.fontWeight = "bold";
                        textElement.style.marginLeft = "-30px";
                        // Apply golden-line styles only for the triangle case
                        goldenLine.style.position = "absolute";
                        goldenLine.style.border = "2px solid gold";
                        goldenLine.style.marginLeft = "-108px";
                        goldenLine.style.zIndex = "2"; // Ensure it stays above the triangle
                        break;

                    case "reverseTriangle":
                        div.className = "upside-down-triangle"; // Apply upside-down triangle styles
                        goldenLine.style.animation = `moveUpsideDownTriangle ${currentDuration} linear infinite`;

                        // Apply text styles only for the upside-down triangle case
                        textElement.style.position = "absolute";
                        textElement.style.color = "white";
                        textElement.style.fontSize = "20px";
                        textElement.style.zIndex = "2";
                        textElement.style.marginTop = "-120px"; // Adjusted for upside-down positioning
                        textElement.style.fontWeight = "bold";
                        textElement.style.marginLeft = "-30px";

                        // Apply golden-line styles only for the upside-down triangle case
                        goldenLine.style.position = "absolute";
                        goldenLine.style.border = "2px solid gold";
                        goldenLine.style.marginLeft = "-108px";
                        goldenLine.style.zIndex = "2"; // Ensure it stays above the triangle

                        break;
                        
                }
  
                animationTimeout = setTimeout(() => {
                    index = (index + 1) % durations.length;
                    animateNextPhase();
                }, durations[index] * 1000);
            }
  