// declarations
let tableID = "contactsTable";
let elementTable = document.getElementById(tableID);
let rowsCounter = elementTable.rows.length;
let buttonCR = "bottomButtonContainer";
let bottomButtonContainer = document.getElementById(buttonCR);
let buttonCreateRowLabel = "createEmptyRow";
let emptyRowButton = document.getElementById(buttonCreateRowLabel);
let tableCellsCounter = elementTable.rows[0].cells.length;
let tdClass = "actionCell";
let nullIndex = 0;

// ---------

rowsNbuttonsNumbering();

emptyRowButton.onclick = () =>
    {
        // console.log("debug on click");
        addNewRow();
    }

// function to add IDs to table rows
// calls buttons numbering
function rowsNbuttonsNumbering()
{
    rowsCounter = elementTable.rows.length;
    for (var index = 0; index < rowsCounter; index++)
    {
        elementTable.rows[index].id = "row" + index;
        buttonsNumbering(index);
    }
}

// function to add IDs to the "Delete" buttons for referencing
// and to add 'onClick' event
function buttonsNumbering(rowNum)
{
    var deleteButton = elementTable.rows[rowNum].querySelector('.actionCell input[type="button"][value="Delete"]');
    if (deleteButton)
        {
            // console.log('onclick parent')
            deleteButton.id = "deleteBtn" + rowNum;
            // console.log(rowNum)
            deleteButton.onclick = () =>
                {
                    elementTable.deleteRow(rowNum);
                    // console.log('onclick');
                    //hideRow(rowNum);
                    rowsCounter = elementTable.rows.length;    
                }
            reArrangeIndices()       
        } 
}

// function to hide table row
// calls adding contact button and re arrange indices
function hideRow(rowNum)
{
    // console.log('hiderow')
    characterName = elementTable.rows[rowNum].cells[2].innerText;
    var confirmation = confirm(`Are you sure you want to delete ${characterName}?`);
    if (confirmation)
        {
            elementTable.rows[rowNum].style.display = 'none';
            addCharBtn(characterName)
            reArrangeIndices()
        }

}

// function to re-arrange the indices of the "index" column
function reArrangeIndices()
{
    var cnt = 0;
    for (var index = 1; index < rowsCounter; index++)
        {
            
            if (window.getComputedStyle(elementTable.rows[index]).display !== 'none')
            {
                cnt++;
                // console.log(index + "," + rowsCounter + "," + cnt);
                elementTable.rows[index].cells[0].innerText = cnt;
                
            }
        }
}

// function to add a button for a hidden contact
function addCharBtn(charName)
{
    var charBtn = document.createElement("input");
    charBtn.type = "button";
    charBtn.id = "showBtn";
    charBtn.value = "Show " + charName;
    bottomButtonContainer.appendChild(charBtn);
    charBtn.onclick = () => 
        {
            charBtn.parentNode.removeChild(charBtn);
            showHiddenRow(charName);
            reArrangeIndices();
            rowsNbuttonsNumbering();
        }
}

// function to show a hidden row
function showHiddenRow(name)
{
    // console.log(name);
    var allRows = document.querySelectorAll('tr');
    allRows.forEach(row => 
        {
            if (row.cells[2].innerText == name)
                {
                    row.style.display = "table-row";
                    return;
                }
        });
}

// function to add an empty row with 'delete' and 'edit' buttons
function addNewRow()
{
    var newRow = elementTable.insertRow(rowsCounter);
    // console.log("row cnt "+rowsCounter);
    for (var index = 0; index < tableCellsCounter; index++)
        {
            newRow.insertCell(index);
        }

    // create all necessary elements    
    var lastCell = newRow.cells[tableCellsCounter - 1];
    lastCell.className = tdClass;
    
    var firstCell = newRow.cells[0];
    var indNum = rowsCounter;

    var actionButtonsDiv = document.createElement("div");
    actionButtonsDiv.className = "actionButtons";

    var deleteButton = document.createElement("input");
    deleteButton.type = "button";
    deleteButton.value = "Delete";

    var editLink = document.createElement("a");
    editLink = "/edit0";
    var editButton = document.createElement("input");
    editButton.type = "button";
    editButton.value = "Edit";
    console.log()
    editButton.onclick = function() {window.location.href = editLink;};

    // add all the elements to the last cell
    actionButtonsDiv.appendChild(deleteButton);
    actionButtonsDiv.appendChild(editButton);
    lastCell.appendChild(actionButtonsDiv);
    firstCell.innerText = indNum;
    rowsCounter = elementTable.rows.length;

    rowsNbuttonsNumbering();
    
}