prefix_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
</head>
<body>
    <div class="container my-4">
        <h1 class="mb-4">{{ title }}</h1>
"""

table_start_template = """
<div id="table-container">
  <table class="table table-striped table-bordered text-nowrap">
    <thead class="thead-dark">
      <tr>
        {% for th in table_headers %}
        <th>{{ th }}</th>
        {% endfor %}
      </tr>
    </thead>
    <tbody>
"""

compressed_top_down_table_data_template = """
{% for depth in depth_problem_map %}
<tr>
  <td>{{ depth }}</td>
  {% for problem,count in depth_problem_map[depth]["distinct"].items() %}
  <td> {{ problem }}, count: {{ count }} </td>
  {% endfor %}  
</tr>
{% endfor %}
"""

top_down_table_data_template = """
{% for depth in depth_problem_map %}
<tr>
  <td><strong>{{ depth }}</strong></td>
  <td>
    <div id="table-container">
      <table class="table table-striped table-bordered text-nowrap">
        <thead class="thead-dark">
          <tr>
            <th>Depth</th>
            <th>Order</th>
            <th>Problem</th>
            <th>Parent Problem</th>
            <th>Dependent Problems</th>
          </tr>
        </thead>
        <tbody>
          {% for order, (fid_problem, fid_parent, problem) in enumerate(depth_problem_map[depth]["nondistinct"]["problems"]) %}
          <tr>
            <td>{{ depth }}</td>
            <td class="text-primary"><strong>{{ order }}</strong></td>
            <td id="{{ hash(fid_problem) }}" class="text-primary"><strong>{{ fid_problem }}</strong></td>
            <td class="text-primary"><strong><a href="#{{ hash(fid_parent) }}">{{ fid_parent }}</a></strong></td>
            <td class="text-secondary">
              <select class="form-select" onchange="topDownSelectOption(this)">
                <option value="" disabled selected>Select an option.</option>
              {% for dependent_problem in depth_problem_map[depth]["nondistinct"]["dependent"][fid_problem] %}
                <option href="#{{ hash(dependent_problem) }}"><em>{{ dependent_problem }}</em></option>
              {% endfor %}
              </select>
            </td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </td>
</tr>
{% endfor %}
"""

bottom_up_table_data_template = """
{% for logical_time,problem in topo_order %}
<tr>
  <td> {{ logical_time }} </td>
  <td> {{ problem }} </td>
  <td> {{ topo_graph[problem]["count"] }} </td>
  {% for dependent_problem in topo_graph[problem]["edges"] %}
  <td> {{ dependent_problem }} </td>
  {% endfor %}  
</tr>
{% endfor %}
"""

problem_dependency_table_data_template = """
<tr>
  <th> {{ problem }} </th>
  {% for dependent_problem in dependent_problems %}
  <td> <em> {{ dependent_problem }} </em> </td>
  {% endfor %}
</tr>
"""

topological_order_table_data_template = """
<tr>
  <th> {{ level }} </th>
  {% for frame in frames %}
  <td> {{ frame }} </td>
  {% endfor %}
</tr>
"""

call_stack_table_data_template = """
<tr>
  <th> {{ logical_time }} </th>
  {% for frame in frames %}
  <td> {{ frame }} </td>
  {% endfor %}
</tr>
"""

table_end_template = """
    </tbody>
  </table>
</div>
"""

suffix_template = """
    </div>
    <!-- Bootstrap JS Bundle -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <script>
        function topDownSelectOption(element) {
            const selectedOption = element.options[element.selectedIndex];

            const url = selectedOption.getAttribute("href");

            // Navigate to the href if it exists
            if (url) {
                console.log(`Selected link: ${url}`);
                // Optionally navigate to the URL
                window.location.href = url;
            } else {
                console.log("No URL found for this option.");
                alret("No href found.")
            }
        }
    </script>
  </body>
</html>
"""
