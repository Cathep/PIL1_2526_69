--
-- Add field jour to demandeouoffre
--
ALTER TABLE `mentoring_requests` ADD COLUMN `jour` varchar(10) NULL;
--
-- Add field heure_debut to demandeouoffre
--
ALTER TABLE `mentoring_requests` ADD COLUMN `heure_debut` time(6) NULL;
--
-- Add field heure_fin to demandeouoffre
--
ALTER TABLE `mentoring_requests` ADD COLUMN `heure_fin` time(6) NULL;
