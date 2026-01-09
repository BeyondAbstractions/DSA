prefix_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
    
    <!-- Prism CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/9000.0.1/themes/prism.min.css" integrity="sha512-/mZ1FHPkg6EKcxo0fKXF51ak6Cr2ocgDi5ytaTBjsQZIH/RNs6GF6+oId/vPe3eJB836T36nXwVh/WBl/cWT4w==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/9000.0.1/plugins/line-highlight/prism-line-highlight.min.css" integrity="sha512-C8oHCUM4bDBqmi+GXg5vQCOjriNXzean+2n2TzTDQoNJDWpjzkkJv5Nl0ZMEQoCKpXrRHpAFztPmClcPCuRdvw==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/9000.0.1/plugins/line-numbers/prism-line-numbers.min.css" integrity="sha512-3/cdM9qaJ5lBlzRKqwhMw+ZcNCVonz66BO6HgJudG/P1azm9wFrru31SsBa4T4Ew1AOH8HfDXSWS6emWwPl42A==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/9000.0.1/plugins/show-language/prism-show-language.min.css" integrity="sha512-09fmad4VA38AJxIRtkrW3DmKI2PsTsEpx3bfR8ZmkQunfQ9jORIieKVREv6fVLmqdnrFbPkCO5PKTnBIIvswBg==" crossorigin="anonymous" referrerpolicy="no-referrer" />
</head>
<body>
    <div class="container my-1">
        <h1 class="text-center mb-4">{{ title }}</h1>
    </div>
    <div class="container">
        <nav class="navbar navbar-light bg-light">
            <div class="container-fluid justify-content-center">
                <a class="btn btn-primary me-1" href="#">{{ title }}</a>
                <div class="btn-group inline-flex gap-1">
                    <a class="btn btn-primary" href="begin.html">
                        &#9654; Begin
                    </a>
                    <a class="btn btn-primary" href="{{ current }}_previous.html">
                        &lt; Previous
                    </a>
                    <a class="btn btn-primary" href="{{ current }}_next.html">
                        &gt; Next
                    </a>
                    <a class="btn btn-primary" href="end.html">
                        &#9209; End
                    </a>
                </div>
            </div>
        </nav>
    </div>
    <hr>
    <div class="container">
        <nav class="navbar navbar-light bg-light">
            <div class="container-fluid justify-content-center mt-1">
                <div class="btn-group inline-flex gap-1">
                    {% for _sid, _sname in sections.items() %}
                        <a class="btn btn-secondary" href="#{{ _sid }}">
                            {{ _sname }}
                        </a>
                    {% endfor %}
                </div>
            </div>
        </nav>
    </div>
    <hr>
"""

section_template = """
<div class="container" id="{{ sid }}">
    <div class="container">
        <nav class="navbar navbar-light bg-light">
            <div class="container-fluid justify-content-center">
                <a class="btn btn-primary me-1" href="#">{{ title }}</a>
                <a class="btn btn-primary me-1" href="#{{ sid }}">{{ sname }}</a>
                <div class="btn-group inline-flex gap-1">
                    <a class="btn btn-primary" href="begin.html#{{ sid }}">
                        &#9654; Begin
                    </a>
                    <a class="btn btn-primary" href="{{ current }}_previous.html#{{ sid }}">
                        &lt; Previous
                    </a>
                    <a class="btn btn-primary" href="{{ current }}_next.html#{{ sid }}">
                        &gt; Next
                    </a>
                    <a class="btn btn-primary" href="end.html#{{ sid }}">
                        &#9209; End
                    </a>
                </div>
            </div>
        </nav>
    </div>
    <div class="container ">
        {{ content|safe }}
    </div>
</div>
<hr>
"""

table_template = """
<table class="table">
    <thead>
        <tr>
            {% for col in columns %}
                <th scope="col">{{ col|e|trim|title }}</th>
            {% endfor %}
        </tr>
    </thead>
    <tbody>
        {% for row in rows %}
            <tr>
                {% for data in row %}
                    <td>{{ data|e }}</td>
                {% endfor %}
            </tr>
        {% endfor %}
    </tbody>
</table>
"""

prism_code_template = """
<pre data-line="{{ data_line }}">
    <code class="language-python" >
{{ code|e }}
    </code>
</pre>
"""


suffix_template = """
     <!-- Prism JS Bundle -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/9000.0.1/prism.min.js" integrity="sha512-UOoJElONeUNzQbbKQbjldDf9MwOHqxNz49NNJJ1d90yp+X9edsHyJoAs6O4K19CZGaIdjI5ohK+O2y5lBTW6uQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.30.0/components/prism-core.min.js" integrity="sha512-Uw06iFFf9hwoN77+kPl/1DZL66tKsvZg6EWm7n6QxInyptVuycfrO52hATXDRozk7KWeXnrSueiglILct8IkkA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.30.0/plugins/autoloader/prism-autoloader.min.js" integrity="sha512-SkmBfuA2hqjzEVpmnMt/LINrjop3GKWqsuLSSB3e7iBmYK7JuWw4ldmmxwD9mdm2IRTTi0OxSAfEGvgEi0i2Kw==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.30.0/plugins/line-numbers/prism-line-numbers.min.js" integrity="sha512-BttltKXFyWnGZQcRWj6osIg7lbizJchuAMotOkdLxHxwt/Hyo+cl47bZU0QADg+Qt5DJwni3SbYGXeGMB5cBcw==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.30.0/plugins/line-highlight/prism-line-highlight.min.js" integrity="sha512-255MpVHZHmxNdOj/PivQ+WSTYFjBxTMfmIszxwsJobUeaoDNUAnAQjYF5TznbiZXrXqpCy8q4QyvJzhykpof3Q==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/9000.0.1/plugins/show-language/prism-show-language.min.js" integrity="sha512-WZeiH/5UJ3HZsxGBbWWIBluPrC/PIHbs/x1GtCP7lky8XbHXEzYfI9PJkL0d7/LdL7DvzHFScNkic8PaNhh+qg==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>

    <!-- Bootstrap JS Bundle -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" crossorigin="anonymous"></script>
  </body>
</html>
"""
