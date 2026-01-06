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
    <link href="https:///prismjs@v1.x/themes/prism.css" rel="stylesheet" />
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
        <ul>
            {% for i in range(lines) %}
                <li> {{ i }} </li>
            {% endfor %}
        </ul>
    </div>
</div>
<hr>
"""


suffix_template = """
     <!-- Prism JS Bundle -->
    <script src="https:///prismjs@v1.x/components/prism-core.min.js"></script>
    <script src="https:///prismjs@v1.x/plugins/autoloader/prism-autoloader.min.js"></script>

     <!-- Bootstrap JS Bundle -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" crossorigin="anonymous"></script>
  </body>
</html>
"""
