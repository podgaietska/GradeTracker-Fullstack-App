const gradingComponents = document.querySelector('#grading-components');
const addComponentBtn = document.querySelector('#add-component');

function createNewComponent() {
    const newComponentDiv = document.createElement('div');
    newComponentDiv.classList.add('grading-component');
    newComponentDiv.classList.add('added-component');
    newComponentDiv.innerHTML = `
    <div class="form-group">
        <select class="form-control" name="grading-component">
            <option name="grading-component" value="">Grading Component</option>
        </select>
    </div>
    <div class="form-group weight">
        <a class="btn remove-component">Remove</a>
        <label for="">Component Weight</label>
        <input type="number" name="weight" class="form-control form-control-sm" step="0.01" min="0" max="1">
    </div>                                
    `
    gradingComponents.appendChild(newComponentDiv);

    $.get('get-grading-components', function(data){
        const selectElement = newComponentDiv.querySelector('select[name="grading-component"]');
    
        data.forEach(function(gradingComponentName){
            const option = document.createElement('option');
            option.value = gradingComponentName;
            option.textContent = gradingComponentName;
            selectElement.appendChild(option);
        })
    })

};


addComponentBtn.addEventListener('click', createNewComponent);

document.addEventListener('click', function (e) {
    // Check if the clicked element has the class .remove-component
    if (e.target.classList.contains('remove-component')) {
        // Access the parent element of the clicked button (the grading component)
        const gradingComponent = e.target.parentElement;
        const elementToRemove = gradingComponent.parentElement;

        // Perform actions to delete the grading component
        // For example, you can remove it from the DOM
        elementToRemove.remove();

        // You can also send an AJAX request to delete it from the server if needed
    }
});