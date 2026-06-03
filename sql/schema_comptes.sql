--
-- Create model Competence
--
CREATE TABLE `skills` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `nom` varchar(150) NOT NULL UNIQUE, `categorie` varchar(100) NOT NULL);
--
-- Create model Filiere
--
CREATE TABLE `fields_of_study` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `nom` varchar(100) NOT NULL UNIQUE, `description` longtext NOT NULL);
--
-- Create model Utilisateur
--
CREATE TABLE `users` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `password` varchar(128) NOT NULL, `last_login` datetime(6) NULL, `is_superuser` bool NOT NULL, `nom` varchar(100) NOT NULL, `prenom` varchar(100) NOT NULL, `email` varchar(254) NOT NULL UNIQUE, `telephone` varchar(20) NOT NULL UNIQUE, `photo_profil` varchar(100) NULL, `bio` longtext NOT NULL, `niveau` varchar(10) NOT NULL, `role` varchar(10) NOT NULL, `est_actif` bool NOT NULL, `date_inscription` datetime(6) NOT NULL, `date_modification` datetime(6) NOT NULL, `token_reinitialisation` varchar(255) NULL, `token_expire_le` datetime(6) NULL, `is_active` bool NOT NULL, `is_staff` bool NOT NULL, `filiere_id` bigint NULL);
CREATE TABLE `users_groups` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `utilisateur_id` bigint NOT NULL, `group_id` integer NOT NULL);
CREATE TABLE `users_user_permissions` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `utilisateur_id` bigint NOT NULL, `permission_id` integer NOT NULL);
--
-- Create model Disponibilite
--
CREATE TABLE `user_availabilities` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `jour` varchar(10) NOT NULL, `heure_debut` time(6) NOT NULL, `heure_fin` time(6) NOT NULL, `utilisateur_id` bigint NOT NULL);
--
-- Create model CompetenceUtilisateur
--
CREATE TABLE `user_skills` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `type_competence` varchar(10) NOT NULL, `niveau` smallint UNSIGNED NOT NULL CHECK (`niveau` >= 0), `competence_id` bigint NOT NULL, `utilisateur_id` bigint NOT NULL);
ALTER TABLE `users` ADD CONSTRAINT `users_filiere_id_45564f3b_fk_fields_of_study_id` FOREIGN KEY (`filiere_id`) REFERENCES `fields_of_study` (`id`);
ALTER TABLE `users_groups` ADD CONSTRAINT `users_groups_utilisateur_id_group_id_8fb7898e_uniq` UNIQUE (`utilisateur_id`, `group_id`);
ALTER TABLE `users_groups` ADD CONSTRAINT `users_groups_utilisateur_id_9dd30a3c_fk_users_id` FOREIGN KEY (`utilisateur_id`) REFERENCES `users` (`id`);
ALTER TABLE `users_groups` ADD CONSTRAINT `users_groups_group_id_2f3517aa_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);
ALTER TABLE `users_user_permissions` ADD CONSTRAINT `users_user_permissions_utilisateur_id_permissio_0c2f85cb_uniq` UNIQUE (`utilisateur_id`, `permission_id`);
ALTER TABLE `users_user_permissions` ADD CONSTRAINT `users_user_permissions_utilisateur_id_1623a084_fk_users_id` FOREIGN KEY (`utilisateur_id`) REFERENCES `users` (`id`);
ALTER TABLE `users_user_permissions` ADD CONSTRAINT `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);
ALTER TABLE `user_availabilities` ADD CONSTRAINT `user_availabilities_utilisateur_id_a54d42aa_fk_users_id` FOREIGN KEY (`utilisateur_id`) REFERENCES `users` (`id`);
ALTER TABLE `user_skills` ADD CONSTRAINT `user_skills_utilisateur_id_competenc_19423378_uniq` UNIQUE (`utilisateur_id`, `competence_id`, `type_competence`);
ALTER TABLE `user_skills` ADD CONSTRAINT `user_skills_competence_id_74591640_fk_skills_id` FOREIGN KEY (`competence_id`) REFERENCES `skills` (`id`);
ALTER TABLE `user_skills` ADD CONSTRAINT `user_skills_utilisateur_id_7f2f6e3d_fk_users_id` FOREIGN KEY (`utilisateur_id`) REFERENCES `users` (`id`);
