# Compression Draco
.PHONY: draco compress-draco clean-draco

# Dossier par défaut
MODELS_DIR = static/public

# Installation des dépendances
install-draco:
	@echo "📦 Installation des dépendances Draco..."
	npm install -g @gltf-transform/cli

# Compresser tous les GLB
compress-draco:
	@echo "🔄 Compression Draco des modèles..."
	@if command -v gltf-transform >/dev/null 2>&1; then \
		for file in $(MODELS_DIR)/*.glb; do \
			if [ -f "$$file" ] && [[ ! "$$file" =~ _draco ]]; then \
				echo "Compressing $$(basename $$file)"; \
				npx gltf-transform draco "$$file" "$${file%.glb}_draco.glb" && \
				mv "$${file%.glb}_draco.glb" "$$file"; \
			fi; \
		done; \
		echo "✅ Compression terminée"; \
	else \
		echo "❌ gltf-transform non installé. Exécutez: make install-draco"; \
	fi

# Compresser un fichier spécifique
compress-%:
	@if [ -f "$(MODELS_DIR)/$*.glb" ]; then \
		echo "🔄 Compression de $*.glb..."; \
		npx gltf-transform draco "$(MODELS_DIR)/$*.glb" "$(MODELS_DIR)/$*_draco.glb" && \
		mv "$(MODELS_DIR)/$*_draco.glb" "$(MODELS_DIR)/$*.glb"; \
		echo "✅ $*.glb compressé"; \
	else \
		echo "❌ Fichier $*.glb non trouvé"; \
	fi

# Nettoyer les backups
clean-draco:
	@echo "🧹 Nettoyage des backups..."
	@rm -f $(MODELS_DIR)/*_draco.glb
	@echo "✅ Nettoyage terminé"
