from flask import Flask, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)

def get_latest_results():
    """
    Extract the latest results from the selenium script execution
    This would typically read from a log file or database
    For now, we'll return the sample data you provided
    """
    # In a real implementation, you'd read this from a log file or database
    # For now, returning the sample data
    return {
        'zb3ZwQnVuZcM0cfCNbQoIQ/': ['000000108', '000000107', '000000106', '000000105', '000000104'],
        'EQl5K9ngclSt6QfdgqaWOQ/': ['000000078', '000000077', '000000076', '000000075', '000000074'],
        'TJOu2PU1eVE4ggj03EvmEA/': ['000000061', '000000060', '000000059'],
        'xOHNlQAHxXOCo0ZZ80tknw/': ['000000065', '000000064'],
        'MXQk7aMKOrU8tSrwloxHag/': ['000000067', '000000066', '000000065'],
        'MgZvDUNpAf59Z8nNKjY34A/': ['000000054', '000000053', '000000052'],
        'AKNx0zBYIaTBbjtKpVg0cg/': ['000000061', '000000060', '000000059'],
        'vMNFGGUkeJCcUm1bnF3kdA/': ['000000051', '000000050', '000000049'],
        'gmjimA9WCpHTavCT8Y99SA/': ['000000056', '000000055', '000000054'],
        'BQ5rCYhC0pU9sCYNvgfLsA/': ['000000048', '000000047', '000000046'],
        'rCQDjfbgNEgddzoNWR0Zcg/': ['000000051', '000000050', '000000049', '000000048'],
        'vmjDkWJaCiLXbkauYw7PeA/': ['000000051', '000000050'],
        'Exg68pTxujyr4xIaohT1dg/': ['000000050', '000000049'],
        'pnSRZsbrNUQqwuE9Q9Tv3g/': ['000000063', '000000062', '000000061', '000000060', '000000059'],
        '5THDQ1wnHRvIgGjIUlOqnA/': ['000000050', '000000049'],
        'Zy19AY3hC3sR7Q0USiwj5w/': ['000000063', '000000062', '000000061', '000000060', '000000059', '000000058'],
        'VdO01hDp4zkgO2Ylv6wgcw/': ['000000061', '000000060', '000000059'],
        'Ok85iau0YPhBTnFOfYarZw/': ['000000057', '000000056', '000000055', '000000054'],
        'FvXrHNoU0tpjCelYqbtD9w/': ['000000056', '000000055', '000000054', '000000053'],
        'hZrOXYcnbylwKmbsVs8lIA/': ['000000056', '000000055', '000000054', '000000053'],
        'JUTbwdhFNqk0kXFfJGGKwA/': ['000000072', '000000071', '000000070', '000000069', '000000068'],
        'OtXaEXl64gDGtW2saOXUZw/': ['000000047', '000000046', '000000045'],
        'R9sv2TMJTnlCnCdk9qdc3Q/': ['000000052', '000000051', '000000050', '000000049'],
        'ABlTscZ34q7CU6Z7p0TUwA/': [],
        'ObCLgchOb2aC6HnsMJIbVA/': ['000000063', '000000062', '000000061', '000000060'],
        'GRAuissfGi7K1CXeQBZvdA/': ['000000060', '000000059', '000000058', '000000057', '000000056'],
        '5HtkrOzkRZCoePzMvkJ3xg/': ['000000057', '000000056', '000000055', '000000054'],
        'IM475uNIONS7uu1kQEK2VQ/': ['000000057', '000000056', '000000055', '000000054'],
        'DQyuJyKAEmhGQcAoQ3x3Mg/': ['000000057', '000000056', '000000055'],
        'ouVVEl9JwUz0ws5gMRwLNQ/': ['000000050', '000000049'],
        'LVjsRgRzmpiyxuWNiOh0lg/': ['000000055', '000000054', '000000053', '000000052', '000000051'],
        's3pIL05Sqsfm2ScDllgbNQ/': ['000000048', '000000047', '000000046'],
        'AMbbNCwUNUX2nUUps9gN4A/': ['000000039', '000000038'],
        'c1b1iwXA4nmixk3DvytdiA/': ['000000054', '000000053', '000000052'],
        'XWAn6pOdfkaNZdmO71BgnA/': ['000000050', '000000049'],
        'gzYveUjjOx25gBJEoiHhEw/': ['000000050', '000000049', '000000048', '000000047'],
        'UJFc11Ho5o1QPJWNrwxhAQ/': ['000000052', '000000051', '000000050', '000000049'],
        'bUniiJRB1It6h3pE30CVfA/': ['000000039', '000000038'],
        'crao2Wv6h5ekVMM7ZInMQA/': ['000000055', '000000054', '000000053', '000000052'],
        'OtK4jH1u6DQMYE8451Lr8A/': ['000000051', '000000050', '000000049', '000000048'],
        '5HtrJ7DW9bYW9Drn5ud80g/': ['000000056', '000000055'],
        'eyMF34dqO3Te9a0Qu4zV4Q/': ['000000048', '000000047', '000000046'],
        '5NP6CL8Fak2PGWsn43Gp0g/': ['000000052', '000000051', '000000050', '000000049'],
        'NIhDkzseUi4XiGR4Yh8l7g/': ['000000060', '000000059', '000000058', '000000057'],
        'Q5GCRyHsM4GZJ4f1OYUkLA/': ['000000059', '000000058'],
        'Bj2hOTDCCbUSxiNX627Unw/': ['000000051', '000000050', '000000049'],
        'FClITJqal67ESpxWJglYjQ/': ['000000043', '000000042'],
        'vM06hslrVVQ3CmcEmisJ2w/': ['000000065', '000000064', '000000063', '000000062'],
        'VtrjgjQSxQkN2vCrTdvHoA/': ['000000052', '000000051', '000000050', '000000049'],
        'HaRj88fFDQql8W10JnGp5Q/': ['000000063', '000000062', '000000061', '000000060']
    }

@app.route('/')
def home():
    return """
    <h1>Phantombuster Results Webhook</h1>
    <p>Available endpoints:</p>
    <ul>
        <li><a href="/results">/results</a> - Get results as JSON</li>
        <li><a href="/results/table">/results/table</a> - Get results as HTML table</li>
        <li><a href="/results/summary">/results/summary</a> - Get summary statistics</li>
    </ul>
    """

@app.route('/results')
def get_results():
    """Return results as JSON"""
    results = get_latest_results()
    return jsonify({
        'status': 'success',
        'timestamp': datetime.now().isoformat(),
        'total_folders': len(results),
        'total_files': sum(len(files) for files in results.values()),
        'results': results
    })

@app.route('/results/table')
def get_results_table():
    """Return results as HTML table"""
    results = get_latest_results()
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Phantombuster Results</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .folder-name {{ font-weight: bold; }}
            .file-count {{ color: #666; }}
            .empty {{ color: #999; font-style: italic; }}
        </style>
    </head>
    <body>
        <h1>Phantombuster Results</h1>
        <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Total folders: {len(results)} | Total files: {sum(len(files) for files in results.values())}</p>
        
        <table>
            <tr>
                <th>Folder Name</th>
                <th>File Count</th>
                <th>File IDs</th>
            </tr>
    """
    
    for folder, files in sorted(results.items()):
        file_count = len(files)
        files_str = ', '.join(files) if files else 'No files'
        empty_class = 'empty' if not files else ''
        
        html += f"""
            <tr>
                <td class="folder-name">{folder}</td>
                <td class="file-count">{file_count}</td>
                <td class="{empty_class}">{files_str}</td>
            </tr>
        """
    
    html += """
        </table>
    </body>
    </html>
    """
    
    return html

@app.route('/results/summary')
def get_results_summary():
    """Return summary statistics"""
    results = get_latest_results()
    
    total_folders = len(results)
    total_files = sum(len(files) for files in results.values())
    folders_with_files = sum(1 for files in results.values() if files)
    empty_folders = total_folders - folders_with_files
    
    # Calculate file count distribution
    file_counts = [len(files) for files in results.values()]
    max_files = max(file_counts) if file_counts else 0
    min_files = min(file_counts) if file_counts else 0
    avg_files = total_files / total_folders if total_folders > 0 else 0
    
    return jsonify({
        'status': 'success',
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_folders': total_folders,
            'total_files': total_files,
            'folders_with_files': folders_with_files,
            'empty_folders': empty_folders,
            'max_files_per_folder': max_files,
            'min_files_per_folder': min_files,
            'avg_files_per_folder': round(avg_files, 2)
        },
        'top_folders_by_file_count': sorted(
            [(folder, len(files)) for folder, files in results.items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
