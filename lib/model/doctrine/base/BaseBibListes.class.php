<?php

/**
 * BaseBibListes
 * 
 * This class has been auto-generated by the Doctrine ORM Framework
 * 
 * @property integer $id_liste
 * @property string $nom_liste
 * @property string $desc_liste
 * @property Doctrine_Collection $CorTaxonliste
 * 
 * @method integer             getIdListe()       Returns the current record's "id_liste" value
 * @method string              getNomListe()      Returns the current record's "nom_liste" value
 * @method string              getDescListe()     Returns the current record's "desc_liste" value
 * @method Doctrine_Collection getCorTaxonliste() Returns the current record's "CorTaxonliste" collection
 * @method BibListes           setIdListe()       Sets the current record's "id_liste" value
 * @method BibListes           setNomListe()      Sets the current record's "nom_liste" value
 * @method BibListes           setDescListe()     Sets the current record's "desc_liste" value
 * @method BibListes           setCorTaxonliste() Sets the current record's "CorTaxonliste" collection
 * 
 * @package    geonature
 * @subpackage model
 * @author     Gil Deluermoz
 * @version    SVN: $Id: Builder.php 7490 2010-03-29 19:53:27Z jwage $
 */
abstract class BaseBibListes extends sfDoctrineRecord
{
    public function setTableDefinition()
    {
        $this->setTableName('taxonomie.bib_listes');
        $this->hasColumn('id_liste', 'integer', 4, array(
             'type' => 'integer',
             'primary' => true,
             'length' => 4,
             ));
        $this->hasColumn('nom_liste', 'string', 50, array(
             'type' => 'string',
             'length' => 50,
             ));
        $this->hasColumn('desc_liste', 'string', null, array(
             'type' => 'string',
             ));
    }

    public function setUp()
    {
        parent::setUp();
        $this->hasMany('CorTaxonliste', array(
             'local' => 'id_liste',
             'foreign' => 'id_liste'));
    }
}