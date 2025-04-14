// This is for admin panel 
document.addEventListener("DOMContentLoaded", function () {
    console.log("Admin JavaScript is working! ✅");  // ✅ Confirm JS is loaded

    function updateFields(row) {
        var shapeField = row.querySelector("[name$='-shape']");
        if (!shapeField) return;

        var inputFields = [
            row.querySelector("[name$='-input1']"),
            row.querySelector("[name$='-input2']"),
            row.querySelector("[name$='-input3']"),
            row.querySelector("[name$='-input4']")
        ];

        var shapeLocks = {
            "Circle": [1, 2, 3],  
            "Square": [1, 2, 3],  
            "Rectangle": [],  
            "Quadrilateral": [],  
            "Triangle": [3],  
            "ReversedTriangle": [3],  
            "Oval": [2, 3]  
        };

        function applyLocking() {
            var selectedShape = shapeField.value;
            var lockedIndexes = shapeLocks[selectedShape] || [];

            inputFields.forEach((input, index) => {
                if (!input) return;

                var parentDiv = input.parentElement;

                if (lockedIndexes.includes(index)) {
                    input.value = "";  // Clear locked field
                    input.setAttribute("disabled", "disabled");

                    // Check if lock icon exists, if not, add it
                    if (!parentDiv.querySelector(".lock-icon")) {
                        var lockIcon = document.createElement("span");
                        lockIcon.classList.add("lock-icon");
                        lockIcon.innerHTML = " 🔒 Locked";
                        lockIcon.style.marginLeft = "10px";
                        lockIcon.style.color = "red";
                        parentDiv.appendChild(lockIcon);
                    }

                    parentDiv.style.opacity = "0.5";  // Grey out locked fields
                } else {
                    input.removeAttribute("disabled");

                    // Remove lock icon if it exists
                    var lockIcon = parentDiv.querySelector(".lock-icon");
                    if (lockIcon) {
                        lockIcon.remove();
                    }

                    parentDiv.style.opacity = "1";  // Restore normal styling
                }
            });
        }

        shapeField.addEventListener("change", applyLocking);
        applyLocking();  // Run on page load
    }

    function applyToAllRows() {
        document.querySelectorAll(".dynamic-exercisephase").forEach(updateFields);
    }

    document.addEventListener("change", applyToAllRows);
    applyToAllRows();  // ✅ Run when page loads
});
