#ifndef _ADAO_GUI_COMPONENT_HXX_
#define _ADAO_GUI_COMPONENT_HXX_

#include <SALOME_Component.hh>
#include "Superv_Component_i.hxx"
#include "ADAO.hh"

class ADAO_GUI_COMPONENT_i:
  public virtual POA_ADAO::ADAO_GUI_COMPONENT,
  public virtual Superv_Component_i
{
  public:
    ADAO_GUI_COMPONENT_i(CORBA::ORB_ptr orb, PortableServer::POA_ptr poa,
                         PortableServer::ObjectId * contId,
                         const char *instanceName, const char *interfaceName);
    ADAO_GUI_COMPONENT_i(CORBA::ORB_ptr orb, PortableServer::POA_ptr poa,
                         Engines::Container_ptr container,
                         const char *instanceName, const char *interfaceName);
    virtual ~ADAO_GUI_COMPONENT_i();

    void destroy();
    CORBA::Boolean init_service(const char * service_name);

    virtual void print_ping();
};

extern "C"
{
    PortableServer::ObjectId * ADAOEngine_factory(CORBA::ORB_ptr orb,
                                                  PortableServer::POA_ptr poa,
                                                  PortableServer::ObjectId * contId,
                                                  const char *instanceName,
                                                  const char *interfaceName);
}
#endif

