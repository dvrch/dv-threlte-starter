/**
 * Service simplifié pour la gestion des URLs d'assets.
 * La logique de construction d'URL a été supprimée car l'API backend
 * fournit maintenant des URLs complètes et fiables directement depuis la base de données.
 */
class AssetService {
  /**
   * Retourne l'URL de l'asset.
   * Si le chemin est déjà une URL complète, il est retourné tel quel.
   * @param path - Le chemin ou l'URL de l'asset.
   */
  public getUrl(path: string): string {
    if (!path) {
      return '';
    }
    // Le backend fournit maintenant des URLs absolues et correctes.
    // Il n'y a plus besoin de construire l'URL côté client.
    return path;
  }
}

export const assets = new AssetService();
