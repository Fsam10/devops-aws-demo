from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Gauge

app = Flask(__name__)
api = Api(app)
CORS(app)

# Prometheus pour les métriques auto
metrics = PrometheusMetrics(app)

# Métriques customisées
asset_count_gauge = Gauge('it_assets_count', 'Nombre total d’actifs IT gérés')
broken_assets_gauge = Gauge('it_assets_status_broken', 'Nombre d’actifs IT en panne')
asset_created_counter = Counter('it_asset_created_total', 'Nombre total d’actifs créés')
asset_deleted_counter = Counter('it_asset_deleted_total', 'Nombre total d’actifs supprimés')

# Stockage temporaire
assets = []
asset_id_counter = 1

class AssetList(Resource):
    def get(self):
        """Lister tous les assets"""
        # MAJ du compteur avant de répondre
        asset_count_gauge.set(len(assets))
        broken_assets_gauge.set(sum(1 for a in assets if a.get('status') == 'broken'))
        return jsonify(assets)

    def post(self):
        """Créer un nouvel asset"""
        global asset_id_counter
        data = request.get_json()
        asset = {
            'id': asset_id_counter,
            'name': data.get('name'),
            'type': data.get('type'),
            'status': data.get('status', 'in_stock'),
            'owner': data.get('owner', None)
        }
        assets.append(asset)
        asset_id_counter += 1
        asset_created_counter.inc()
        asset_count_gauge.set(len(assets))
        if asset['status'] == 'broken':
            broken_assets_gauge.inc()
        return jsonify(asset)

class Asset(Resource):
    def get(self, asset_id):
        for asset in assets:
            if asset['id'] == asset_id:
                return jsonify(asset)
        return jsonify({'message': 'Asset not found'}), 404

    def put(self, asset_id):
        for asset in assets:
            if asset['id'] == asset_id:
                data = request.get_json()
                old_status = asset['status']
                asset.update({
                    'name': data.get('name', asset['name']),
                    'type': data.get('type', asset['type']),
                    'status': data.get('status', asset['status']),
                    'owner': data.get('owner', asset['owner']),
                })
                # Met à jour le gauge broken si statut changé
                broken_assets_gauge.set(sum(1 for a in assets if a.get('status') == 'broken'))
                return jsonify(asset)
        return jsonify({'message': 'Asset not found'}), 404

    def delete(self, asset_id):
        global assets
        to_delete = next((a for a in assets if a['id'] == asset_id), None)
        if to_delete:
            assets = [a for a in assets if a['id'] != asset_id]
            asset_deleted_counter.inc()
            asset_count_gauge.set(len(assets))
            broken_assets_gauge.set(sum(1 for a in assets if a.get('status') == 'broken'))
            return jsonify({'message': f'Asset {asset_id} deleted'})
        return jsonify({'message': 'Asset not found'}), 404

api.add_resource(AssetList, '/assets')
api.add_resource(Asset, '/assets/<int:asset_id>')

if __name__ == '__main__':
    from werkzeug.middleware.dispatcher import DispatcherMiddleware
    from prometheus_client import make_wsgi_app

    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })

    app.run(host="0.0.0.0", port=5000, debug=True)
