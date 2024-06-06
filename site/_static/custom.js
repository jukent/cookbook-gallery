function getClassOfCheckedCheckboxes(checkboxes) {
  var tags = [];
  checkboxes.forEach(function (cb) {
    if (cb.checked) {
      tags.push(cb.getAttribute("rel"));
    }
  });
  return tags;
}
  
function change() {
  console.log("Change event fired.");
  var domainsCbs = document.querySelectorAll(".domains input[type='checkbox']");
  var packagesCbs = document.querySelectorAll(".packages input[type='checkbox']");

  var domainTags = getClassOfCheckedCheckboxes(domainsCbs);
  var packageTags = getClassOfCheckedCheckboxes(packagesCbs);

  var filters = {
    domains: domainTags,
    packages: packageTags
  };

  filterResults(filters);
}
  
function filterResults(filters) {
  console.log("Filtering results...");
  var rElems = document.querySelectorAll(".tagged-card");

  rElems.forEach(function (el) {
    var isVisible = true; // Assume visible by default

    // Check if the element has any domain or package filter
    if (filters.domains.length > 0 || filters.packages.length > 0) {
      var hasMatchingDomain = false;
      var hasMatchingPackage = false;

      // Check if the element matches at least one selected domain filter
      if (filters.domains.length > 0) {
        hasMatchingDomain = filters.domains.some(function (domain) {
          return el.classList.contains(domain);
        });
      } else {
        // If no domain filters are selected, assume it matches
        hasMatchingDomain = true;
      }

      // Check if the element matches at least one selected package filter
      if (filters.packages.length > 0) {
        hasMatchingPackage = filters.packages.some(function (package) {
          return el.classList.contains(package);
        });
      } else {
        // If no package filters are selected, assume it matches
        hasMatchingPackage = true;
      }

      // The element should be visible if it matches any filter within each category
      isVisible = hasMatchingDomain && hasMatchingPackage;
    }

    // Toggle visibility based on the result
    if (isVisible) {
      el.classList.remove("d-none");
      el.classList.add("d-flex");
    } else {
      el.classList.remove("d-flex");
      el.classList.add("d-none");
    }
  });
}

var checkboxes = document.querySelectorAll('input[type="checkbox"]');
  checkboxes.forEach(function (checkbox) {
    checkbox.addEventListener("change", change);
    });
  
console.log("Script loaded.");