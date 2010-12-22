#include <string>
#include <iostream>
#include "adaogui_component.hxx"

using namespace std;

//! Constructor for component "cppcompos" instance
/*!
 *
 */
ADAO_GUI_COMPONENT_i::ADAO_GUI_COMPONENT_i(CORBA::ORB_ptr orb,
                                           PortableServer::POA_ptr poa,
                                           PortableServer::ObjectId * contId,
                                           const char *instanceName,
                                           const char *interfaceName)
: Superv_Component_i(orb, poa, contId, instanceName, interfaceName)
{
  _thisObj = this ;
  _id = _poa->activate_object(_thisObj);
}

ADAO_GUI_COMPONENT_i::ADAO_GUI_COMPONENT_i(CORBA::ORB_ptr orb,
                                           PortableServer::POA_ptr poa,
                                           Engines::Container_ptr container,
                                           const char *instanceName,
                                           const char *interfaceName)
: Superv_Component_i(orb, poa, container, instanceName, interfaceName)
{
  _thisObj = this ;
  _id = _poa->activate_object(_thisObj);
}

void 
ADAO_GUI_COMPONENT_i::destroy()
{
  Engines_Component_i::destroy();
}

CORBA::Boolean
ADAO_GUI_COMPONENT_i::init_service(const char * service_name)
{
  CORBA::Boolean rtn = true;
  return rtn;
}

void
ADAO_GUI_COMPONENT_i::print_ping()
{
  std::cerr << "ADAO_GUI_COMPONENT_i ping" << std::endl;
}
//! Destructor for component "ADAO_GUI_COMPONENT_i" instance
ADAO_GUI_COMPONENT_i::~ADAO_GUI_COMPONENT_i()
{
}

extern "C"
{
  PortableServer::ObjectId * ADAOEngine_factory(CORBA::ORB_ptr orb,
                                                PortableServer::POA_ptr poa,
                                                PortableServer::ObjectId * contId,
                                                const char *instanceName,
                                                const char *interfaceName)
  {
    MESSAGE("PortableServer::ObjectId * ADAOEngine_factory()");
    ADAO_GUI_COMPONENT_i * myEngine = new ADAO_GUI_COMPONENT_i(orb, poa, contId, instanceName, interfaceName);
    return myEngine->getId() ;
  }
}

