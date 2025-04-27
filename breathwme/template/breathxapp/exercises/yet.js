<script>
    // Get exercise phases data from Django
const phasesData = {{ phases_data|safe }};

// DOM elements
const shapeElement = document.getElementById('shape-element');
const ball = document.getElementById('ball');
const debugPath = document.getElementById('debug-path');
const phaseInfo = document.querySelector('.phase-info');
const phaseProgress = document.getElementById('phase-progress');
const cycleProgress = document.getElementById('cycle-progress');
const startBtn = document.getElementById('start-btn');
const pauseBtn = document.getElementById('pause-btn');
const resetBtn = document.getElementById('reset-btn');

// Current state
let currentPhaseIndex = 0;
let currentBreathingPhaseIndex = 0;
let currentEdgeIndex = 0;
let currentCycle = 1;
let isRunning = false;
let timer = null;
let animationId = null;

// Ball animation parameters
let ballPosition = 0;
let animationStartTime = null;
let animationDuration = 5000; // Default duration (ms)

// Path coordinates for each shape
const shapePaths = {};

// Edge segments for multi-edge shapes
const shapeEdges = {};

// Initialize
updateShapeDisplay();

// Event listeners
startBtn.addEventListener('click', startExercise);
pauseBtn.addEventListener('click', pauseExercise);
resetBtn.addEventListener('click', resetExercise);

function startExercise() {
    if (!isRunning) {
        isRunning = true;
        startBtn.disabled = true;
        pauseBtn.disabled = false;
        resetBtn.disabled = false;
        runCurrentEdge();
    }
}

function pauseExercise() {
    if (isRunning) {
        isRunning = false;
        clearTimeout(timer);
        cancelAnimationFrame(animationId);
        startBtn.disabled = false;
        startBtn.textContent = 'Resume';
    }
}

function resetExercise() {
    isRunning = false;
    clearTimeout(timer);
    cancelAnimationFrame(animationId);
    currentPhaseIndex = 0;
    currentBreathingPhaseIndex = 0;
    currentEdgeIndex = 0;
    currentCycle = 1;
    startBtn.disabled = false;
    startBtn.textContent = 'Start';
    pauseBtn.disabled = true;
    resetBtn.disabled = true;
    ball.style.display = 'none';
    updateShapeDisplay();
}

function runCurrentEdge() {
    if (!isRunning) return;
    
    const phase = phasesData[currentPhaseIndex];
    if (!phase) {
        // Exercise completed
        resetExercise();
        phaseProgress.textContent = 'Exercise completed!';
        return;
    }
    
    // Create path for the current shape if it doesn't exist
    createShapePath(phase.shape);
    
    // Get total number of edges for this shape
    const totalEdges = getEdgeCount(phase.shape);
    
    // Get current breathing phase
    const breathingPhases = phase.breathing_phases;
    const currentBreathingPhase = breathingPhases[currentBreathingPhaseIndex];
    
    // For shapes with multiple edges, each edge corresponds to a breathing phase
    // For circular shapes (circle/oval), there are only two phases for the full circuit
    const isCircularShape = ['circle', 'oval'].includes(phase.shape.toLowerCase());
    
    // Get duration for current edge/phase
    let duration;
    if (isCircularShape) {
        // For circle/oval, use the specified duration for each half (inhale/exhale)
        duration = phase.inputs[currentBreathingPhaseIndex] || 0;
    } else {
        // For other shapes, duration is the same for all edges
        duration = phase.inputs[0] || 0;
    }
    
    // Update display
    updateBreathingPhaseDisplay(phase.shape, currentBreathingPhase, duration);
    
    // Calculate start and end positions for the animation
    // For multi-edge shapes, we animate one edge at a time
    let startPosition = isCircularShape ? 
        (currentBreathingPhaseIndex / breathingPhases.length) : 
        (currentEdgeIndex / totalEdges);
    
    let endPosition = isCircularShape ? 
        ((currentBreathingPhaseIndex + 1) / breathingPhases.length) : 
        ((currentEdgeIndex + 1) / totalEdges);
    
    // Start ball animation for this edge
    startBallAnimation(phase, startPosition, endPosition, duration);
    
    // Schedule next edge
    timer = setTimeout(() => {
        goToNextEdge(phase);
    }, duration * 1000);
}

function getEdgeCount(shape) {
    switch(shape.toLowerCase()) {
        case 'circle':
        case 'oval':
            return 1; // Circular shapes are treated specially
        case 'triangle':
        case 'reversedtriangle':
            return 3;
        case 'square':
        case 'rectangle':
        case 'quadrilateral':
            return 4;
        default:
            return 1;
    }
}

function goToNextEdge(phase) {
    const isCircularShape = ['circle', 'oval'].includes(phase.shape.toLowerCase());
    const totalEdges = getEdgeCount(phase.shape);
    
    // Update breathing phase index
    currentBreathingPhaseIndex = (currentBreathingPhaseIndex + 1) % phase.breathing_phases.length;
    
    // For non-circular shapes, update edge index
    if (!isCircularShape) {
        currentEdgeIndex = (currentEdgeIndex + 1) % totalEdges;
        
        // If we've completed all edges, increment cycle
        if (currentEdgeIndex === 0) {
            currentCycle++;
        }
    } else {
        // For circular shapes, if we've completed all breathing phases, increment cycle
        if (currentBreathingPhaseIndex === 0) {
            currentCycle++;
        }
    }
    
    // Check if we completed all cycles for this shape
    if (currentCycle > phase.cycles) {
        currentCycle = 1;
        currentEdgeIndex = 0;
        currentBreathingPhaseIndex = 0;
        currentPhaseIndex++;
    }
    
    runCurrentEdge();
}

function updateBreathingPhaseDisplay(shape, breathingPhase, duration) {
    // Clear previous classes
    shapeElement.className = '';
    
    // Set shape class
    shapeElement.classList.add(shape.toLowerCase());
    
    // Update text displays
    phaseInfo.textContent = breathingPhase;
    phaseProgress.textContent = `Phase: ${currentPhaseIndex + 1}/${phasesData.length} - ${breathingPhase} (${duration}s)`;
    cycleProgress.textContent = `Cycle: ${currentCycle}/${phasesData[currentPhaseIndex].cycles}`;
}

function updateShapeDisplay() {
    const phase = phasesData[currentPhaseIndex];
    if (!phase) return;
    
    // Clear previous classes
    shapeElement.className = '';
    
    // Set shape class
    shapeElement.classList.add(phase.shape.toLowerCase());
    
    // Reset text displays
    phaseInfo.textContent = 'Ready';
    phaseProgress.textContent = 'Ready to start';
    cycleProgress.textContent = `Phase: ${currentPhaseIndex + 1}/${phasesData.length}`;
    
    // Create path for the shape
    createShapePath(phase.shape);
}

function createShapePath(shape) {
    // Don't recreate if already exists
    if (shapePaths[shape]) return;
    
    // Get shape element dimensions
    const shapeRect = shapeElement.getBoundingClientRect();
    const containerRect = document.querySelector('.shape-container').getBoundingClientRect();
    
    // Adjust coordinates to be relative to container
    const offsetX = shapeRect.left - containerRect.left;
    const offsetY = shapeRect.top - containerRect.top;
    
    // Path points array
    let points = [];
    let edges = [];
    
    switch(shape.toLowerCase()) {
        case 'circle':
            // Create points around a circle
            const circleRadius = shapeRect.width / 2;
            const centerX = offsetX + circleRadius;
            const centerY = offsetY + circleRadius;
            
            for (let i = 0; i <= 100; i++) {
                const angle = (i / 100) * Math.PI * 2;
                const x = centerX + Math.cos(angle) * circleRadius;
                const y = centerY + Math.sin(angle) * circleRadius;
                points.push({ x, y });
            }
            break;
            
        case 'square':
            // Create points around a square
            const squareLeft = offsetX;
            const squareTop = offsetY;
            const squareRight = offsetX + shapeRect.width;
            const squareBottom = offsetY + shapeRect.height;
            
            // Top edge (left to right)
            const topEdge = [];
            for (let x = squareLeft; x <= squareRight; x += 5) {
                topEdge.push({ x, y: squareTop });
            }
            
            // Right edge (top to bottom)
            const rightEdge = [];
            for (let y = squareTop; y <= squareBottom; y += 5) {
                rightEdge.push({ x: squareRight, y });
            }
            
            // Bottom edge (right to left)
            const bottomEdge = [];
            for (let x = squareRight; x >= squareLeft; x -= 5) {
                bottomEdge.push({ x, y: squareBottom });
            }
            
            // Left edge (bottom to top)
            const leftEdge = [];
            for (let y = squareBottom; y >= squareTop; y -= 5) {
                leftEdge.push({ x: squareLeft, y });
            }
            
            // Store edges separately for phase tracking
            edges = [topEdge, rightEdge, bottomEdge, leftEdge];
            points = [...topEdge, ...rightEdge, ...bottomEdge, ...leftEdge];
            break;
            
        case 'rectangle':
            // Create points around a rectangle
            const rectLeft = offsetX;
            const rectTop = offsetY;
            const rectRight = offsetX + shapeRect.width;
            const rectBottom = offsetY + shapeRect.height;
            
            // Top edge (left to right)
            const rectTopEdge = [];
            for (let x = rectLeft; x <= rectRight; x += 5) {
                rectTopEdge.push({ x, y: rectTop });
            }
            
            // Right edge (top to bottom)
            const rectRightEdge = [];
            for (let y = rectTop; y <= rectBottom; y += 5) {
                rectRightEdge.push({ x: rectRight, y });
            }
            
            // Bottom edge (right to left)
            const rectBottomEdge = [];
            for (let x = rectRight; x >= rectLeft; x -= 5) {
                rectBottomEdge.push({ x, y: rectBottom });
            }
            
            // Left edge (bottom to top)
            const rectLeftEdge = [];
            for (let y = rectBottom; y >= rectTop; y -= 5) {
                rectLeftEdge.push({ x: rectLeft, y });
            }
            
            // Store edges separately for phase tracking
            edges = [rectTopEdge, rectRightEdge, rectBottomEdge, rectLeftEdge];
            points = [...rectTopEdge, ...rectRightEdge, ...rectBottomEdge, ...rectLeftEdge];
            break;
            
        case 'oval':
            // Create points around an oval
            const ovalRadiusX = shapeRect.width / 2;
            const ovalRadiusY = shapeRect.height / 2;
            const ovalCenterX = offsetX + ovalRadiusX;
            const ovalCenterY = offsetY + ovalRadiusY;
            
            for (let i = 0; i <= 100; i++) {
                const angle = (i / 100) * Math.PI * 2;
                const x = ovalCenterX + Math.cos(angle) * ovalRadiusX;
                const y = ovalCenterY + Math.sin(angle) * ovalRadiusY;
                points.push({ x, y });
            }
            break;
            
        case 'triangle':
            // Create points for an equilateral triangle
            const triWidth = 250;
            const triHeight = 216;
            
            // Calculate the three points of the triangle
            const triLeft = offsetX;
            const triTop = offsetY;
            
            const point1 = { x: triLeft + triWidth/2, y: triTop }; // Top
            const point2 = { x: triLeft, y: triTop + triHeight }; // Bottom-left
            const point3 = { x: triLeft + triWidth, y: triTop + triHeight }; // Bottom-right
            
            // Create path segments
            // Left edge (top to bottom-left)
            const leftSegmentPoints = createLinePoints(point1, point2, 50);
            // Bottom edge (bottom-left to bottom-right)
            const bottomSegmentPoints = createLinePoints(point2, point3, 50);
            // Right edge (bottom-right to top)
            const rightSegmentPoints = createLinePoints(point3, point1, 50);
            
            edges = [leftSegmentPoints, bottomSegmentPoints, rightSegmentPoints];
            points = [...leftSegmentPoints, ...bottomSegmentPoints, ...rightSegmentPoints];
            break;
            
        case 'reversedtriangle':
            // Create points for a reversed equilateral triangle
            const revTriWidth = 250;
            const revTriHeight = 216;
            
            // Calculate the three points of the triangle
            const revTriLeft = offsetX;
            const revTriTop = offsetY;
            
            const revPoint1 = { x: revTriLeft + revTriWidth/2, y: revTriTop + revTriHeight }; // Bottom
            const revPoint2 = { x: revTriLeft, y: revTriTop }; // Top-left
            const revPoint3 = { x: revTriLeft + revTriWidth, y: revTriTop }; // Top-right
            
            // Create path segments
            // Right edge (bottom to top-right)
            const revRightSegmentPoints = createLinePoints(revPoint1, revPoint3, 50);
            // Top edge (top-right to top-left)
            const revTopSegmentPoints = createLinePoints(revPoint3, revPoint2, 50);
            // Left edge (top-left to bottom)
            const revLeftSegmentPoints = createLinePoints(revPoint2, revPoint1, 50);
            
            edges = [revRightSegmentPoints, revTopSegmentPoints, revLeftSegmentPoints];
            points = [...revRightSegmentPoints, ...revTopSegmentPoints, ...revLeftSegmentPoints];
            break;
            
        case 'quadrilateral':
            // Create points for a diamond (rotated square)
            const diamondSize = 200;
            const diamondCenterX = offsetX + shapeRect.width / 2;
            const diamondCenterY = offsetY + shapeRect.height / 2;
            
            // Calculate the four points of the rotated square
            const dTop = { x: diamondCenterX, y: diamondCenterY - diamondSize/2 };
            const dRight = { x: diamondCenterX + diamondSize/2, y: diamondCenterY };
            const dBottom = { x: diamondCenterX, y: diamondCenterY + diamondSize/2 };
            const dLeft = { x: diamondCenterX - diamondSize/2, y: diamondCenterY };
            
            // Create path segments
            // Top-right edge
            const topRightPoints = createLinePoints(dTop, dRight, 25);
            // Bottom-right edge
            const bottomRightPoints = createLinePoints(dRight, dBottom, 25);
            // Bottom-left edge
            const bottomLeftPoints = createLinePoints(dBottom, dLeft, 25);
            // Top-left edge
            const topLeftPoints = createLinePoints(dLeft, dTop, 25);
            
            edges = [topRightPoints, bottomRightPoints, bottomLeftPoints, topLeftPoints];
            points = [...topRightPoints, ...bottomRightPoints, ...bottomLeftPoints, ...topLeftPoints];
            break;
            
        default:
            // Default fallback for any unsupported shapes
            const fallbackRadius = Math.min(shapeRect.width, shapeRect.height) / 2;
            const fallbackCenterX = offsetX + shapeRect.width / 2;
            const fallbackCenterY = offsetY + shapeRect.height / 2;
            
            for (let i = 0; i <= 100; i++) {
                const angle = (i / 100) * Math.PI * 2;
                const x = fallbackCenterX + Math.cos(angle) * fallbackRadius;
                const y = fallbackCenterY + Math.sin(angle) * fallbackRadius;
                points.push({ x, y });
            }
    }
    
    // Store the path and edges
    shapePaths[shape] = points;
    shapeEdges[shape] = edges.length > 0 ? edges : [points];
}

function createLinePoints(start, end, numPoints) {
    const points = [];
    for (let i = 0; i <= numPoints; i++) {
        const ratio = i / numPoints;
        const x = start.x + (end.x - start.x) * ratio;
        const y = start.y + (end.y - start.y) * ratio;
        points.push({ x, y });
    }
    return points;
}

function drawDebugPath(points) {
    // Clear previous path
    while (debugPath.firstChild) {
        debugPath.removeChild(debugPath.firstChild);
    }
    
    if (points.length < 2) return;
    
    // Create a path element
    const pathElement = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    
    // Build path data
    let pathData = `M ${points[0].x} ${points[0].y}`;
    for (let i = 1; i < points.length; i++) {
        pathData += ` L ${points[i].x} ${points[i].y}`;
    }
    pathData += ' Z'; // Close the path
    
    // Set path attributes
    pathElement.setAttribute('d', pathData);
    pathElement.setAttribute('stroke', 'red');
    pathElement.setAttribute('stroke-width', '2');
    pathElement.setAttribute('fill', 'none');
    
    // Add path to SVG
    debugPath.appendChild(pathElement);
    debugPath.style.opacity = '0.5'; // Make visible for debugging
}

function startBallAnimation(phase, startPosition, endPosition, duration) {
    const shape = phase.shape;
    
    // Show the ball
    ball.style.display = 'block';
    
    // Convert duration to milliseconds
    animationDuration = duration * 1000;
    animationStartTime = null;
    ballPosition = 0; // Reset ball position for this segment
    
    // Start animation loop
    cancelAnimationFrame(animationId);
    animationId = requestAnimationFrame((timestamp) => 
        animateBall(timestamp, shape, startPosition, endPosition));
}

function animateBall(timestamp, shape, startPosition, endPosition) {
    if (!animationStartTime) animationStartTime = timestamp;
    if (!isRunning) return;
    
    const elapsedTime = timestamp - animationStartTime;
    const progress = Math.min(elapsedTime / animationDuration, 1);
    
    // Calculate current position within the segment
    const segmentPosition = startPosition + (endPosition - startPosition) * progress;
    
    // Position the ball
    positionBallOnPath(shape, segmentPosition);
    
    // Continue animation if not complete
    if (progress < 1) {
        animationId = requestAnimationFrame((timestamp) => 
            animateBall(timestamp, shape, startPosition, endPosition));
    }
}

function positionBallOnPath(shape, position) {
    // Make sure path exists for this shape
    if (!shapePaths[shape]) {
        createShapePath(shape);
    }
    
    const path = shapePaths[shape];
    if (!path || path.length === 0) return;
    
    // Calculate point index based on position (0 to 1)
    const pointIndex = Math.floor(position * (path.length - 1));
    
    // Get the point from the path
    if (pointIndex >= 0 && pointIndex < path.length) {
        const point = path[pointIndex];
        
        // Position the ball
        ball.style.left = `${point.x}px`;
        ball.style.top = `${point.y}px`;
    }
}

// Wait for DOM to be fully loaded before calculating initial paths
window.addEventListener('load', () => {
    if (phasesData && phasesData.length > 0) {
        const initialShape = phasesData[0].shape;
        // Create path for the initial shape after a small delay to ensure DOM is ready
        setTimeout(() => createShapePath(initialShape), 100);
    }
});

// Update paths when window is resized
window.addEventListener('resize', () => {
    // Clear existing paths
    Object.keys(shapePaths).forEach(key => delete shapePaths[key]);
    Object.keys(shapeEdges).forEach(key => delete shapeEdges[key]);
    
    // Recreate path for current shape
    if (phasesData && phasesData.length > 0) {
        const currentShape = phasesData[currentPhaseIndex].shape;
        createShapePath(currentShape);
    }
});
</script>