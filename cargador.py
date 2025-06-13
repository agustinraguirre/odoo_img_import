import os #Este módulo de Python te permite interactuar con el sistema operativo
import base64 #Codificar las imágenes en texto antes de enviarlas a Odoo por XML-RPC
import xmlrpc.client #Este módulo permite a Python comunicarse con servidores XML-RPC,
from PIL import Image #(Pillow) es una biblioteca de Python para trabajar con imágenes.

# CONFIGURACIÓN

ODOO_URL = '...'
ODOO_DB = '...'
ODOO_USER = '...'
ODOO_PASSWORD = '...'
LOCAL_FOLDER = r'....'

# CONEXIÓN A ODOO

common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASSWORD, {})
models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')

# FUNCIÓN PRINCIPAL

def cargar_imagenes():
    contador = 0
    errores = 0
    archivos = os.listdir(LOCAL_FOLDER)

    for filename in archivos:
        try:
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                print(f"❌ No es una imagen válida: {filename}")
                continue

            sku = filename.split(' (')[0].split('.')[0]  # "SKU123 (1).jpg" 

            path = os.path.join(LOCAL_FOLDER, filename)

            # Validar que se pueda abrir como imagen
            try:
                with Image.open(path) as img:
                    img.verify()
            except Exception as e:
                print(f"❌ Archivo dañado o inválido como imagen: {filename}")
                errores += 1
                continue

            with open(path, 'rb') as f:
                imagen_base64 = base64.b64encode(f.read()).decode('utf-8')

            producto_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
                'product.template', 'search',
                [[['default_code', '=', sku]]])

            if not producto_ids:
                print(f"⚠️ Producto no encontrado para SKU: {sku}")
                errores += 1
                continue

            producto_id = producto_ids[0]

            # Verificar si es imagen principal o adicional
            if ' (' not in filename:
                # Imagen principal
                models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
                    'product.template', 'write',
                    [[producto_id], {'image_1920': imagen_base64}])
                print(f"✅ Imagen principal cargada para {sku}")
            else:
                # Evitar duplicados
                imagenes_existentes = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
                    'product.image', 'search_read',
                    [[['product_tmpl_id', '=', producto_id]]],
                    {'fields': ['name']})

                if any(img['name'] == filename for img in imagenes_existentes):
                    print(f"🔁 Imagen ya existente, se omite: {filename}")
                    continue

                # Imagen adicional
                models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
                    'product.image', 'create',
                    [{
                        'product_tmpl_id': producto_id,
                        'name': filename,
                        'image_1920': imagen_base64,
                    }])
                print(f"🖼️ Imagen adicional cargada para {sku}")

            contador += 1

        except Exception as e:
            print(f"❌ Error procesando {filename}: {e}")
            errores += 1

    print("🔚 Carga finalizada.")
    print(f"✅ Total imágenes cargadas: {contador}")
    print(f"⚠️ Total errores: {errores}")

# EJECUCIÓN

if __name__ == "__main__":
    cargar_imagenes()
